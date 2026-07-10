# SDAD Doctor Architecture And Diagnostic Contract

Status: Scope approved; written design pending owner review; implementation deferred
Date: 2026-07-10

## Scope

This design covers only two changes:

1. a reusable diagnostic architecture for downstream SDAD projects;
2. the read-only `sdad doctor` diagnostic contract.

The design preserves the v3.0 state model. It does not add a packet status,
scale, intensity, autonomy level, evidence tier, or owner authority.

The following work is deliberately out of scope:

- a worked product example;
- comparative or effectiveness benchmarking;
- command execution, auto-fix, or state migration;
- tool-specific overlays or a dynamic check plug-in system;
- model calls, semantic AI review, network access, or telemetry;
- a new README diagram or another explanatory image.

## Existing Contracts To Preserve

The implementation must preserve these repository contracts:

- `sdad-state.yaml` version 1 and its documented packet statuses;
- the existing error strings produced by
  `collect_agent_experience_violations()` for repository fixtures;
- the no-dependency Python validation path;
- normalized repository-relative POSIX paths for routed files;
- the separation between AI progress and owner acceptance;
- the rule that `owner_gates` contains only gates capable of stopping the
  current packet.

`evidence_ready` and `completed` are not current packet statuses and must not
be introduced by the doctor. The doctor must reason using the existing
statuses, including `ai_complete`, `software_verified`, `owner_accepted`,
`release_candidate`, and `production_ready`.

## Design 1/4: Architecture And Boundaries

### Decision

Use a shared validation core with a thin command-line adapter. Keep only the
abstractions that isolate filesystem access, deterministic policy, diagnostic
rules, and output data.

```text
scripts/sdad.py
    |
    v
DiagnosticEngine
    |-- ProjectView
    |-- DoctorPolicy
    |-- fixed DiagnosticCheck sequence
    `-- DoctorReport[Finding]

agent_experience.py ---> shared state_contract.py <--- state-schema check
```

The command line owns argument parsing, rendering, and exit codes. It does not
contain diagnostic rules. The engine owns check order and report aggregation.
Checks do not print, exit, mutate files, invoke commands, or access global
configuration.

### Proposed File Layout

```text
scripts/
|-- sdad.py
`-- sdad_validator/
    |-- diagnostics.py
    |-- doctor.py
    |-- project_view.py
    |-- state_contract.py
    `-- checks/
        |-- __init__.py
        |-- state_schema.py
        |-- path_integrity.py
        |-- packet_coherence.py
        |-- owner_gates.py
        `-- review_state.py
```

Checks are grouped by stable domain, not split into a class for every small
rule. The engine uses an explicit ordered tuple of built-in checks. Version 1
has no discovery mechanism, entry points, dependency-injection container, YAML
rule language, or third-party plug-in API.

### Core Data Contracts

`Finding` is an immutable diagnostic record with:

- `id`: stable machine-readable rule identifier;
- `severity`: `error` or `warning`;
- `message`: concise human explanation;
- `path`: repository-relative POSIX path when applicable;
- `line`: optional one-based source line;
- `evidence`: the observed value or contradiction;
- `remediation`: the smallest safe correction.

The same `id` may occur for more than one path. A finding occurrence is
identified by `id`, `path`, and `line` together.

`DoctorReport` contains the resolved project root, ordered findings, run and
skipped check names, and error/warning counts. It contains data only and can be
rendered as human text or JSON without rerunning checks.

`DoctorPolicy` contains deterministic inputs that otherwise make tests depend
on the host:

- current date;
- stale-state threshold, default 30 days;
- maximum state size, default 64 KiB;
- maximum inspected control-document size, default 1 MiB;
- the conservative Q5 keyword set used only for warnings.

Policy is injectable by tests and internal callers. Version 1 does not add a
project policy file or CLI flags for these values.

`ProjectView` is the only filesystem boundary exposed to checks. It provides
confined UTF-8 reads, regular-file checks, and normalized path resolution. The
production implementation is `FilesystemProjectView`; tests may use an
in-memory implementation. It does not expose arbitrary shell execution or
unbounded directory traversal.

`DiagnosticCheck` has one operation: consume the project view, parsed state,
and policy, then return findings. A check must be deterministic for those
inputs. This protocol exists for separation and testing, not as a public
plug-in system.

### Shared State Contract

Move the state-specific constants and pure parsing/validation logic currently
embedded in `agent_experience.py` into `state_contract.py`.

Both callers use the same core:

- repository validation checks the canonical template and converts state
  issues back to its current violation strings;
- `sdad doctor` checks a downstream project's root-level `sdad-state.yaml` and
  converts state issues to `Finding` records.

This prevents template validation and downstream validation from silently
developing different enums, required keys, or path rules. Refactoring the
existing validator must be behavior-preserving before doctor-only rules are
added.

### State Parsing Boundary

Do not add PyYAML or select a parser based on what happens to be installed.
Environment-dependent parsing would make a no-clone diagnostic inconsistent.

The shared core accepts the canonical SDAD YAML subset emitted by the version 1
template:

- top-level scalar mappings;
- the two-space-indented `active_packet` mapping;
- block lists of scalars and mappings;
- the empty list form `[]`;
- plain, single-quoted, and double-quoted scalar values;
- comments outside quoted values.

It rejects anchors, aliases, tags, merge keys, tabs for indentation, multiline
scalars, arbitrary flow collections, and unknown indentation as
`state.syntax.unsupported`. Unsupported input must never be partially accepted
as a valid state. Parsing preserves source lines so duplicate keys and malformed
items can be reported precisely.

### Filesystem And Trust Boundary

The doctor is read-only and treats project content as untrusted input.

- The project root is the explicit positional path or the current directory.
- The doctor does not search parent directories for a more convenient root.
- State routes must use normalized relative POSIX paths.
- Absolute paths, drive-qualified paths, backslashes, `.` segments, and `..`
  segments are rejected before filesystem access.
- Resolved files must remain under the resolved project root. Symlink or
  junction escape is an error.
- Only regular UTF-8 text files within configured size limits are inspected.
- The doctor performs no subprocess, Git, validation-command, network, write,
  or owner-approval action.

This confinement reduces accidental reads but is not advertised as an OS
sandbox against a concurrently mutating hostile filesystem.

### Execution Flow

1. The CLI validates invocation and constructs the filesystem view.
2. The engine reads and parses `sdad-state.yaml` once.
3. State syntax and schema checks run first.
4. Checks whose prerequisites are satisfied run in a fixed order.
5. Checks with unavailable prerequisites are recorded as skipped.
6. Findings are sorted by check order, path, line, and identifier.
7. The CLI renders the completed report and selects the exit code.

A missing state file is a completed diagnostic with an error finding. An
unreadable or invalid project root prevents diagnosis and is an invocation or
environment failure. An unexpected check exception must not be converted into
a clean report.

## Design 2/4: `sdad doctor` Diagnostic Contract

### Invocation

```text
python <SDAD_CHECKOUT>/scripts/sdad.py doctor [PROJECT_ROOT] [--json] [--strict]
```

- `PROJECT_ROOT` defaults to the current directory.
- `--json` emits one versioned JSON document and no human prose on stdout.
- `--strict` makes warnings fail the command without changing their severity.
- Version 1 has no `--fix`, `--run`, `--execute-validation`, or network mode.

Version 1 is checkout-only. The command runs from an SDAD repository checkout
against another project path. Existing adapter and no-clone installers do not
install `scripts/sdad.py`, and no-clone documentation must not advertise the
doctor until a separate distribution design is approved.

### Applicability

Version 1 diagnoses a stateful SDAD control plane. It applies to Standard and
Full projects, plus any Mini project that deliberately adopted
`sdad-state.yaml`. A valid One-shot or stateless Mini workflow does not invoke
the doctor.

The CLI cannot reliably distinguish a valid stateless workflow from a broken
stateful project. Therefore, once explicitly invoked, a missing
`sdad-state.yaml` is `state.missing` and exit `1`. Automatic applicability
detection and a stateless-project success mode are out of scope.

### Exit Codes

| Code | Meaning |
|---|---|
| `0` | Diagnosis completed with no errors; warnings are allowed unless `--strict` is set. |
| `1` | Diagnosis completed and found an error, or found a warning under `--strict`. |
| `2` | Invalid invocation, unusable project root, OS-level failure opening the required state file, or internal diagnostic failure prevented a complete diagnosis. |

A missing `sdad-state.yaml` produces `state.missing` and exit `1`; it does not
produce exit `2`. In JSON mode, an exit `2` failure still emits one versioned
JSON error object so automation does not have to parse human stderr.

The I/O boundary is explicit: failure to open the root or required state file
is exit `2`; bytes that were read successfully but exceed the limit, are not
valid UTF-8, or contain unsupported syntax produce findings and exit `1`.
Failure to read an optional review/TODO document produces a `path.unreadable`
finding and skips only its dependent check.

### Severity Rule

Use `error` only when the control plane cannot be trusted or contains a direct
contradiction. Use `warning` when the state may be stale, incomplete, heuristic,
or requires human review but remains structurally usable.

`--strict` changes process success, not finding classification. There is no
`info` severity in version 1.

### Check Contract

#### 1. State Syntax And Schema

Errors:

- missing `sdad-state.yaml`;
- `sdad-state.yaml` exceeds the 64 KiB state limit;
- unsupported syntax or invalid UTF-8;
- duplicate keys at any supported mapping level;
- missing required v3 control keys;
- wrong scalar, mapping, or list shape;
- unsupported scale, intensity, autonomy, or packet status;
- missing or blank packet `id`, `objective`, or `status`;
- malformed validation, owner-gate, or route list entries;
- an explicit state `version` other than `1`.

Warnings:

- missing `version`, retained for legacy state compatibility;
- unknown top-level keys, which are preserved but not interpreted.

The required operational keys remain `scale`, `intensity`, `autonomy`,
`active_spec`, `active_packet`, `owner_gates`, `validation`, and
`routed_docs`. `updated` is checked by the freshness rule rather than treated
as a schema error.

Collection entries have one canonical shape:

- `owner_gates`: non-empty scalar strings;
- `validation`: mappings whose `command` and `proves` keys, when present, have
  scalar values; duplicate keys are schema errors and unknown keys are schema
  warnings;
- `routed_docs`: non-empty scalar path strings.

Schema checks own container shape, key type, scalar type, and duplicate keys.
The validation-contract check alone owns missing, blank, and placeholder
`command`/`proves` values so the same defect cannot receive two severities.

#### 2. Path Integrity

Errors:

- invalid or non-normalized `active_spec` or `routed_docs` path;
- path resolution outside the project root, including link escape;
- routed target missing or not a regular file;
- routed target declared for content inspection but inaccessible to the OS;
- inspected control-document bytes that are not valid UTF-8;
- `active_spec` missing or not a regular file.

Warnings:

- duplicate entries in `routed_docs`.
- an optional review or TODO control document exceeds the 1 MiB inspection
  limit; the dependent coherence check is skipped.

The doctor checks the declared routes only. It does not crawl the repository to
guess additional active documentation.

#### 3. Validation Contract

Warnings outside the validation-required status set:

- an empty validation list;
- a blank command;
- a blank or missing `proves` value;
- template placeholder text instead of a runnable project command or claim.

For this check, the validation-required status set is exactly
`software_verified`, `tester_ready`, `hardware_evidence_received`,
`hardware_verified`, `owner_accepted`, `release_candidate`, and
`production_ready`. The same incomplete conditions are errors in those
statuses.

The doctor validates the evidence contract but never runs its commands. A
passing doctor therefore means the state is coherent, not that product tests
passed.

#### 4. Freshness

Warnings:

- missing `updated`;
- `updated: YYYY-MM-DD` or another placeholder;
- an invalid calendar date;
- a date more than 30 days older than the injected current date;
- a date more than one day in the future.

Freshness uses the declared state date, not filesystem modification time. The
finding includes the observed date and calculated age when available.

#### 5. Packet And Owner-Gate Coherence

Errors:

- `autonomy: 4` has no current owner gate while the status is `not_started`,
  `in_progress`, `ai_complete`, `software_verified`, `tester_ready`,
  `hardware_evidence_received`, `hardware_verified`, or `blocked`;
- `production_ready` still lists a gate capable of stopping the same active
  packet;
- a verification-bearing status has an invalid validation contract.

Warnings:

- `owner_accepted` still lists a gate for the same packet; the owner may have
  accepted a narrower named scope, so the doctor requests reconciliation
  instead of declaring the state invalid.

`scale: full` is not an error signal by itself. Full can be selected for
duration, collaboration, or evidence complexity without a Q5 gate. A Q5 term
found only in free text is also not enough for an error. If the objective
contains a conservative release, production, migration, destructive-action,
real-data, auth, money, security, rollback, or equivalent Q5 term while gates
are empty, the doctor emits a warning for owner review. This rule is explicitly
heuristic and may not upgrade or accept risk. Matching is case-insensitive and
uses token or phrase boundaries, never raw substring matching.

Version 1 does not infer a gate error from `release_candidate` alone. Current
source documents describe it both as having every named release gate passed
and as being candidate-ready with known gates pending release review. That
source-contract ambiguity must be reconciled before the doctor enforces gate
presence or absence for this status.

#### 6. Review And TODO Coherence

Deterministic cross-file checks use an optional explicit packet marker:

```text
[packet:WP-001]
```

The literal `packet` is lowercase and case-sensitive. The captured ID is the
non-empty text before the next `]`, trimmed at both ends, and must equal
`active_packet.id` exactly and case-sensitively. An active packet ID containing
`]` cannot be represented and produces a warning instead of guessed linkage.

The doctor reads only `review-findings.md` and
`docs/TODO-Open-Items.md` when those files exist inside the project or are
declared routes.

Parsing is deliberately narrow:

- an active finding is a line beginning `- ` between
  `## Active Findings` and the next level-two heading;
- a classified finding uses exactly
  `- [Critical] [packet:WP-001] description`, with `High`, `Medium`, and `Low`
  as the other accepted classifications;
- an unclassified linked finding uses exactly
  `- [packet:WP-001] description`;
- an active TODO is a line beginning `- [ ] ` under `## Active Work` or
  `## Release / Production Readiness`; its linked form uses exactly
  `- [ ] [packet:WP-001] description`;
- `## Future / Deferred`, checked boxes, prose, and the template's
  `None currently tracked.` sentinel are not active work;
- a missing required section produces a structure warning and skips that
  document's coherence rules instead of being interpreted as zero open work.

Status sets are exact:

- coherence-sensitive, non-terminal: `software_verified`, `tester_ready`,
  `hardware_evidence_received`, `hardware_verified`, and `release_candidate`;
- terminal for this coherence check: `owner_accepted` and
  `production_ready`.

Errors:

- an active finding linked to the current packet remains under
  `## Active Findings` while the packet has a terminal status;
- an unchecked TODO linked to the current packet remains open in those same
  terminal statuses;
- a current-packet `Critical` finding remains active at
  `release_candidate`.

Warnings:

- linked active findings or unchecked TODOs remain in a coherence-sensitive,
  non-terminal status;
- terminal packet status coexists with active unlinked findings or TODOs, so
  packet relevance cannot be proved automatically;
- the current packet ID cannot be represented by the marker grammar.

At `release_candidate`, `packet.open-critical-finding` supersedes the general
`packet.open-finding` warning so one line does not produce duplicate findings.

The doctor must not infer linkage from similar prose. Without the explicit
marker it may request manual review, but it may not claim a contradiction.

### Stable Finding Identifiers

Version 1 permits only the identifiers below:

| Domain | Identifier | Severity behavior |
|---|---|---|
| State input | `state.missing` | Error |
| State input | `state.too-large` | Error |
| State input | `state.encoding.invalid` | Error |
| State syntax | `state.syntax.unsupported` | Error |
| State schema | `state.schema.duplicate-key` | Error |
| State schema | `state.schema.missing-key` | Error |
| State schema | `state.schema.unknown-key` | Warning |
| State schema | `state.schema.wrong-kind` | Error |
| State schema | `state.schema.missing-version` | Warning |
| State schema | `state.schema.unsupported-version` | Error |
| State schema | `state.schema.unsupported-value` | Error |
| Packet schema | `state.packet.missing-field` | Error |
| Packet schema | `state.packet.blank-field` | Error |
| Collection schema | `state.collection.malformed-entry` | Error |
| Freshness | `state.updated.missing` | Warning |
| Freshness | `state.updated.placeholder` | Warning |
| Freshness | `state.updated.invalid` | Warning |
| Freshness | `state.updated.stale` | Warning |
| Freshness | `state.updated.future` | Warning |
| Path | `path.invalid` | Error |
| Path | `path.outside-root` | Error |
| Path | `path.missing` | Error |
| Path | `path.not-file` | Error |
| Path | `path.unreadable` | Error |
| Path | `path.encoding.invalid` | Error |
| Path | `path.too-large` | Warning |
| Path | `path.duplicate-route` | Warning |
| Validation | `validation.empty` | Warning outside the validation-required set; error inside it |
| Validation | `validation.missing-command` | Warning outside the validation-required set; error inside it |
| Validation | `validation.blank-command` | Warning outside the validation-required set; error inside it |
| Validation | `validation.missing-proves` | Warning outside the validation-required set; error inside it |
| Validation | `validation.blank-proves` | Warning outside the validation-required set; error inside it |
| Validation | `validation.placeholder` | Warning outside the validation-required set; error inside it |
| Validation | `validation.unknown-key` | Warning |
| Owner gate | `gate.required` | Error |
| Owner gate | `gate.q5-review` | Warning |
| Owner gate | `gate.pending-after-acceptance` | Warning for `owner_accepted`; error for `production_ready` |
| Review structure | `review.structure.missing-section` | Warning |
| TODO structure | `todo.structure.missing-section` | Warning |
| Packet linkage | `packet.open-finding` | Warning in a non-terminal verification status; error in a terminal status |
| Packet linkage | `packet.open-critical-finding` | Error at `release_candidate` |
| Packet linkage | `packet.open-todo` | Warning in a non-terminal verification status; error in a terminal status |
| Packet linkage | `packet.unlinked-open-work` | Warning in a terminal status |
| Packet linkage | `packet.marker.unrepresentable` | Warning |

No unlisted finding identifier may appear while `schema_version` is `1`.
Identifiers and JSON field names are compatibility surfaces. Human messages
may be clarified without changing an identifier's meaning or severity rule.

### Human Output

Human output is deterministic plain text and ends with a count summary. Color
is not required in version 1.

```text
ERROR path.missing docs/required.md
  Observed: routed_docs contains a file that does not exist.
  Fix: correct the route or create the intended control document.

WARNING state.updated.stale sdad-state.yaml:2
  Observed: updated is 45 days old.
  Fix: reconcile the current packet and record today's date.

Doctor: 1 error, 1 warning, 5 checks run, 1 skipped
```

### JSON Output

JSON uses this stable top-level shape:

```json
{
  "schema_version": 1,
  "root": "C:/work/project",
  "strict": false,
  "summary": {
    "errors": 1,
    "warnings": 1
  },
  "checks": {
    "run": ["state_schema", "path_integrity"],
    "skipped": ["review_state"]
  },
  "findings": [
    {
      "id": "path.missing",
      "severity": "error",
      "path": "docs/required.md",
      "line": null,
      "message": "A routed document does not exist.",
      "evidence": "routed_docs contains docs/required.md",
      "remediation": "Correct the route or create the intended file."
    }
  ]
}
```

JSON paths use forward slashes. Findings and check names retain deterministic
ordering across operating systems. Host-specific absolute paths appear only in
the top-level `root` field.

An exit `2` JSON result uses the same top-level fields, empty findings for
failures that occur before checks, and one additional field:

```json
"diagnostic_error": {
  "kind": "unusable_root",
  "message": "The project root cannot be inspected."
}
```

`diagnostic_error` is absent when diagnosis completes, including normal exit
`1` reports. Version 1 permits exactly four `diagnostic_error.kind` values:
`invalid_invocation`, `unusable_root`, `unreadable_state`, and
`internal_error`.

### Test And Compatibility Requirements

Implementation is acceptable only when all of the following are true:

- state parsing and every diagnostic family have focused pure unit tests;
- tests use an in-memory project view for rule isolation;
- CLI integration tests cover human output, JSON output, strict mode, and all
  three exit codes;
- path tests cover POSIX paths, Windows drive/backslash input, `..`, symlink or
  junction escape where supported, missing files, and Unicode paths;
- clock tests prove the 30-day boundary without using the host date;
- malformed state never produces a false-clean report;
- existing repository-validator violation strings remain unchanged;
- the complete existing test suite, repository validator, and
  `git diff --check` pass on Linux and Windows.

No result from `sdad doctor` may be described as proof of method effectiveness,
runtime correctness, release approval, or owner acceptance. It proves only the
specified control-plane consistency checks.

## Rejected Alternatives

### Standalone Doctor Script With Duplicated Rules

Rejected because state enums and path rules would drift from repository
validation.

### Full Plug-In Or Dependency-Injection Framework

Rejected because version 1 has a fixed, small check set and no evidence that
third-party rule discovery is needed.

### PyYAML Or Optional Parser Selection

Rejected because it adds installation friction or changes behavior depending
on the host environment.

### Auto-Fix Or Validation Command Execution

Rejected because mutation and subprocess execution would expand the trust
boundary, blur diagnosis with implementation, and risk manufacturing evidence
or owner approval.

## Implementation Gate

This document authorizes design review only. It does not authorize doctor code,
template changes, `[packet:...]` rollout, installer changes, or release work.
Implementation begins only after the owner approves this written design and a
separate implementation plan.
