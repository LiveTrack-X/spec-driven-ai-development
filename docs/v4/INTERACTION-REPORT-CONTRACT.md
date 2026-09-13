# Optional interaction reports v1

Status: SDAD 4.0 W2 implementation candidate, based on state v2 and Inspector
snapshot v2. This is an optional Markdown reporting convention, not a new
authority ledger, agent runtime, approval channel, or released protocol version.

## Authoring and authority

Use the existing authoritative document for each fact: accepted requirements in
active SPEC, interpretation/choices in implementation notes or ADR, remaining
work in TODO/findings, and checks in the existing evidence record. Add the opt-in
marker `<!-- sdad-interactions:1 -->` to documents containing structured reports.
The document must already be reachable through the bounded SDAD document route.
Use one top-level `sdad-interaction` fenced JSON object per record. Nested fenced
examples are ignored. Keep current reports small enough for the existing 48 KiB /
500-line reader; archive history through existing project conventions.

Record only externally reportable conclusions, assumptions, choices and results.
Do not record private internal reasoning. A source reference is a pointer, not
proof of user authority. The current user instruction and active SPEC still
control. Update on start, important correction/decision, verification or handoff;
do not emit a record for every tool call.

## Common fields

| Field | Contract |
| --- | --- |
| `version` | Integer `1`; independent from state/Doctor/snapshot/product versions |
| `id` | Unique record ID; duplicate IDs are conflicts, never latest-wins |
| `kind` | `request`, `interpretation`, `progress`, `decision`, `response` |
| `packet`, `request_id` | Exact target; identifiers use ASCII letters/digits and `._:-`, max 160 |
| `base_revision` | Explicit requirement revision ID; change when intended scope changes |
| `author`, `reported_at` | Self-reported author and timezone-qualified ISO timestamp |
| `summary` | Short explicit report, not Inspector-generated interpretation |
| `supersedes` | Optional prior report ID; explicit reconciliation, not time ordering |

Strings are nonempty and at most 4000 characters. JSON duplicate keys and unknown
versions are rejected. Unknown fields are ignored by consumers; they cannot
override Inspector-generated source or link status. Inspector reads at most 100
reports from the existing bounded document set. Unreadable or truncated reporting
sources are incomplete; a missing profile is unreported. Existing raw document
view remains available. Reports from other packets are not current reports.

## Kind-specific fields

- `request`: required `source_ref` pointing to the user instruction or normative
  requirement. Keep one current record per `request_id`; historical revisions must
  not compete as current declarations. `summary` is a short attributed excerpt or
  description; it does not establish additional authorization.
- `interpretation`: optional `scope`, `excluded`, `assumptions`, `remaining` string
  arrays. Multiple current interpretations conflict unless an explicit supersedes
  chain identifies a single current report. Each array has at most 30 items.
- `progress`: optional `criteria` with `id`, `summary`, `status` (`remaining`,
  `implemented_reported`, `verification_reported`, `blocked`), plus `remaining`.
  These are reports, not automatic lifecycle updates or completion percentages.
- `decision`: optional `reason`, `alternatives`, `impact`, `owner_question`.
  A question does not create approval; independent authorized work continues.
- `response`: required `correction_id` and `stage`: `acknowledged`, `planned`,
  `applied`, `verification_reported`. Include understood change and affected scope
  in summary/impact. When the requirement changes, keep the original baseline and
  correction ID, and link the current requirement with `result_revision` on applied
  or verification reports. A response to an older resulting revision remains stale.
  Verification reports require a nonempty `evidence` array of
  `{ "path": "project-relative source", "result": "actual result and limits" }`.
  Declared commands alone do not satisfy this requirement. Evidence is displayed
  as AI-reported evidence; Inspector never runs checks or upgrades owner acceptance.

Evidence links open only documents already available through the bounded reader;
outside paths and network references are not fetched. Report provenance includes
the actual document path, fence line and SHA-256 of read content. `reported_at`
and Inspector `observed_at` remain separate. Neither proves semantic accuracy.

## Projection compatibility

The existing `/api/documents` envelope gains optional `interactions` with its own
`schema_version: 1`, `project_root`, `packet`, `observed_at`, `status`, `records`
and `issues`. This does not add fields to snapshot v2. Legacy consumers ignore
the optional member; new consumers render missing/unknown projection versions
as unreported/unsupported and preserve document browsing. State and Doctor
remain unchanged. Custom adapters can omit the projection.

Matching requires exact project, packet, request and requirement revision.
Duplicate IDs, competing current records and unresolved references cannot
establish current completion. Never select by timestamp or ID order. Older
responses are visible as stale when inspected, never responses to a newer ID.

## Correction drafts and manual transport

Inspector stores drafts in its own application data, scoped by canonical project,
packet and request. Save is explicit. Each correction has a stable UUID, original
interpretation, correction text, base revision, and optional superseded correction
ID. A request is sealed immutably before clipboard exposure; `sealed` means copy
success is unconfirmed. Sealed/copied requests cannot change content; new edits
get a new ID. Re-copy retains ID. This prevents a failed post-copy storage update
from allowing different text to reuse an exposed ID.

The full generated request is reviewable before copying. Copying is not delivery,
acknowledgment, application, process stop, protected-action approval or acceptance.
The user delivers the request using their existing agent conversation. That agent
updates the authoritative project documents and writes a matching response report.
Inspector re-scan reads it; only that exact correction ID and baseline can advance
the displayed report stage. No elapsed-time success or hidden transmission exists.

Draft storage is bounded to 40 records and fails without discarding existing data
when full. Persistent history editing/retention UX is follow-up scope. Direct
transport, user acceptance writes and agent control remain W6/later contracts.

## Minimal hand-authored example (reference, not a current report)

````markdown
<!-- sdad-interactions:1 -->
```sdad-interaction
{"version":1,"id":"request-save","kind":"request","packet":"P1","request_id":"save","base_revision":"save-r1","author":"agent citing user","reported_at":"2026-09-08T00:00:00Z","summary":"Keep settings after reopening","source_ref":"SPEC/SPEC-COMPLETE.md#save"}
```
```sdad-interaction
{"version":1,"id":"interpret-save","kind":"interpretation","packet":"P1","request_id":"save","base_revision":"save-r1","author":"agent","reported_at":"2026-09-08T00:01:00Z","summary":"Restore in the same browser","excluded":["Cross-device sync"]}
```
```sdad-interaction
{"version":1,"id":"ack-C1","kind":"response","packet":"P1","request_id":"save","base_revision":"save-r1","author":"agent","reported_at":"2026-09-08T00:02:00Z","summary":"Received: same account across devices","correction_id":"correction-C1","stage":"acknowledged","impact":["Account-scoped server persistence required"]}
```
````
