# Documentation Governance Method Field Note

Status: Active reference
Scope: Reusable operating patterns extracted from a documentation-heavy AI project

This note extracts the development method, not product internals. This field
pattern is useful because it shows how a large AI-assisted project can keep many
SPEC revisions, active docs, reviews, hardening tracks, and owner decisions from
collapsing into chat memory.

## What This Pattern Teaches

### 1. Start From A Compact Control Plane

This pattern requires every agent to start from the installed tool adapter,
then `sdad-state.yaml`, then `docs/INDEX.md` before touching code, SPECs,
prompts, or documentation. The index is not a passive table of contents. It is
the repository router:

- which docs are active,
- which docs are historical,
- which docs are only product notes,
- which SPEC files are current,
- which backlog and review files must be read.

Reusable rule: every serious AI-driven project needs a compact state plus one
current navigation document that answers "what should this agent read now?"

### 2. Keep A Mandatory Router, Not Mandatory Full Reads

The recommended agent entry sequence is:

1. load the installed tool adapter,
2. read the compact active-state file,
3. read the documentation index,
4. inspect current source/tests,
5. read one current path routed by the state and index,
6. load policy, playbooks, archives, or evidence only on demand.

Reusable rule: never let a fresh AI session begin from an old handoff, archived
plan, or impressive SPEC without first checking the current route.

Reusable context-stability rule: the start route is a routing requirement, not
a full-read requirement. Confirm authorization before reading private data;
size limits do not grant access. Before reading large state files, old handoffs,
logs, generated artifacts, authorized private data, or archives, check size and
use bounded reads.
Use local soft triggers such as 50 KB or 500 lines for bounded reads, 200 KB or
2,000 lines for a context-stability check, and avoid full startup reads above
1 MB unless the owner asks for historical reconstruction.

### 3. Define Authority By Fact Type

This pattern separates facts that a single precedence list would conflate:

- source, migrations, tests, runtime, and repeatable commands establish observed
  behavior and implementation status;
- the state-declared `active_spec` establishes intended scope, behavior, and
  acceptance criteria;
- state and active ledgers establish current execution and unresolved work;
- an authoritative owner-decision record controls its declared authorization or
  acceptance;
- handoffs carry continuity pointers only;
- proposed SPECs, references, archives, filenames, dates, and chat are not
  current authority.

Read order is routing, not authority. Owner decisions control scope, risk
tolerance, protected actions, and acceptance only for their recorded boundary.
Provider chat memory or AI confidence remains context only, never current authority.

`SPEC-COMPLETE.md` is an integrated baseline rather than an automatic override.
A second SPEC is normative only where the active entrypoint incorporates it or
after a packet transaction changes that pointer. ADRs record rationale, not a
hidden replacement for normative acceptance. Read order is routing, not
authority. Owner acceptance does not upgrade weak
evidence.

If a SPEC spans past-to-present history, current active sections override older
sections. Older sections remain useful rationale but should not drive new
implementation unless reaffirmed in the active route.

### 4. Split Current Work From Review Findings

This pattern uses different files for different kinds of unfinished work:

- `docs/TODO-Open-Items.md` tracks open implementation work.
- `review-findings.md` tracks active defects, hardening findings, and review
  backlog.
- `docs/implementation-notes.md` tracks current spec-unstated implementation
  decisions that are not defects, TODOs, or ADRs.
- archived docs preserve rationale but do not drive current implementation.

Reusable rule: do not bury bugs in prose handoffs. Give defects a durable
review ledger, implementation gaps a durable TODO ledger, and spec-unstated
implementation rationale a bounded implementation-notes surface.

### 5. Require Documentation Consistency Checks

Use minimum documentation update sets. A code change that touches security,
configuration, retrieval, worker lifecycle, prompts, roadmap status, or open gap
status should imply a specific set of docs to check or update before reporting.

Reusable rule: every implementation packet report must say either which docs
changed or which docs were checked and why no content change was needed. Create
a handoff only when another session needs continuity.

### 6. Separate Core Completion From Production Readiness

This pattern distinguishes "feature-rich v1 candidate" from "production-ready."
Production readiness is its own hardening track covering security, migration
proof, backup safety, observability, scale evidence, runtime settings policy,
and rollback posture.

Reusable rule: completion percentages must name the scope. A project can be
mostly implemented for local/core use while still not production-ready.

### 7. Promote External Ideas Deliberately

Keep external references and adoption notes under product-note routes until they
are promoted into active SPECs. This prevents interesting research from silently
becoming required work.

Reusable rule: future ideas need a promotion step before builders treat them as
implementation requirements.

### 8. Use Evidence-Based Status, Not AI Confidence

Status is strongest when tied to focused test commands, migration checks, audit
commands, docs checked, and known remaining gaps. AI confidence is not a valid
completion artifact by itself.

Reusable rule: ask every builder and reviewer to include commands run, results,
files changed, docs checked, implementation notes if SPEC gaps affected the
implementation, and remaining risks.

## Reusable Documentation Governance Rule Pack

Add these rules to projects with heavy docs, many SPEC revisions, or multiple AI
sessions:

- A single `docs/INDEX.md` must route all active docs and archives.
- `docs/Repository-Operating-Rules.md` must collect repeated rules that would
  otherwise stay in chat.
- The installed tool adapter must require the first-read chain.
- The first-read chain must apply context-stability before loading routed files.
- `docs/TODO-Open-Items.md` and `review-findings.md` must stay active and
  separate.
- `docs/implementation-notes.md` must capture spec-unstated implementation
  decisions without becoming a raw reasoning transcript.
- Historical docs must be preserved but clearly excluded from the execution path.
- Code changes must include a documentation consistency check.
- Production readiness must be a named gate, not an assumption.

## When To Use This Pattern

Use documentation-governance controls when:

- the project has long-lived SPECs,
- multiple AI sessions or models will contribute,
- the owner needs progress visibility without writing code,
- docs are likely to multiply,
- production-readiness claims are risky,
- external research can easily overwhelm active implementation.
