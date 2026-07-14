# AI Work Loop

SDAD expands to SPEC-Directed AI Development. It is a repository-local
operating protocol around the work, not a prescribed implementation method.
TDD, direct implementation, external planning workflows, and tool-native
features may all operate inside the declared boundary.

Use one loop for SDAD Protocol work:

```text
Plan -> Route -> Implement -> Verify -> Report
                       |                 |
                       +-> Owner Gate    +-> Handoff, when needed
```

Owner gates and handoffs are triggered branches, not mandatory phases. Use the
smallest loop that preserves the validation contract and owner control.

## Plan

Normalize the request into one executable boundary:

- outcome or objective,
- authority or reference,
- allowed scope and constraints,
- validation and required evidence,
- owner gates and stop conditions,
- report format.

The current applicable owner instruction overrides an older owner direction.
If it redirects affected work, stop the old direction, re-enter Plan -> Route,
and reconcile the new intent into SPEC/state before stateful implementation
resumes. An explicit current owner command authorizes only its named direction,
acceptance, or protected action for the stated boundary; persist it and do not
ask for the same decision again. It does not waive evidence, prerequisites,
tool policy, or a different protected action. Review/reference-only intent remains read-only.

Infer and report scale, execution scope, claim boundary, owner gates, and the
assumptions behind them from the request and repository first. Ask at most one
blocking question only when an unresolved fact would change objective/direction,
authority/reference role, execution boundary, protected action/gate, or claim
boundary. Recommend a default with the question; otherwise proceed.

## Route

For a stateful project, read:

```text
adapter -> sdad-state.yaml -> docs/INDEX.md
```

Then select only the source, test, path, heading, active section, or targeted
match needed for the current intent. `routed_docs` is an eligible selection set,
not a read-all list. Report the routed documents actually read.
An owner-named current input may be inspected within the request even when a
stale route omits it. If adopted, update the active authority and routes before
stateful implementation.

## Implement

Work within `execution_scope: unit | packet`. A unit is one review-worthy
change slice. A packet may contain related units and is the default Standard and
Full boundary. Do not pause for micro-approval inside an authorized boundary.

Give each fact one authoritative home:

| Fact | Authority |
|---|---|
| Intended scope, behavior, or acceptance criteria | state-declared `active_spec` |
| Observed behavior | current source, tests, runtime, and reproducible commands |
| Small non-spec implementation decision | implementation notes |
| Hard-to-reverse architecture decision | ADR |
| Unresolved work | TODO or finding |
| Owner authorization or acceptance | one authoritative owner-decision record |
| Evidence and claim status | evidence matrix or claim registry, linked to that decision |
| Cross-session recovery links/results | handoff |
| Current execution state | `sdad-state.yaml` |

`SPEC-COMPLETE.md` is an integrated baseline, not an immutable or automatically
active document. For stateful work, `active_spec` is the single normative SPEC
entrypoint. A SPEC supplied as current requirements is a change request unless
the owner limits it to review/draft/reference; reconcile it before affected work.
A merely discovered file gains no authority from its name, date, or status.
Keep a non-terminal packet only for a change inside the same unfinished
acceptance boundary, and invalidate affected evidence. A material change or a
change after owner acceptance starts a new, never-reused packet ID; it does not
rewrite the accepted packet's history.

## Verify

Bind validation to the packet before implementation. For state v2,
`validation_for` must equal `active_packet.id`. Run the named checks and retain
bounded evidence, limits, and unverified areas.

Evidence-ready is not owner-accepted. Doctor green proves structural
consistency only. A successful task benchmark proves that task only. An
improvement claim requires a controlled comparison.

## Long-Running Re-entry And Loop Exceptions

`active_packet.status` is the current dominant checkpoint, not a cumulative
history of implementation, evidence, and acceptance. Preserve those facts in
their own authorities. Re-enter Plan -> Route whenever a new fact can change
scope, evidence, gates, or the next action:

| Event | Required decision |
|---|---|
| Owner changes, narrows, or replaces the current direction | stop affected local and delegated work; classify the instruction as additive or replacing, re-plan/re-route, and treat old-boundary outputs as stale until reconciled and revalidated |
| Owner cancels the packet without replacement | stop affected work; mark the packet `deferred`, preserve partial evidence and the cancellation reason in a packet-linked record, set the resume trigger to explicit owner reactivation, and never auto-resume |
| Clarification within the same unfinished acceptance boundary | keep the packet; amend the active SPEC only for intended behavior or acceptance criteria, otherwise use implementation notes; invalidate affected evidence |
| Owner directs adoption/implementation of a new or conflicting SPEC | treat it as a current change request; hold affected work, then amend the same non-terminal packet or switch to a new packet according to the acceptance boundary |
| Owner asks to review/compare/explain a SPEC | keep the request read-only; report conflicts without incorporating, switching packets, or implementing |
| Unrequested additional SPEC is discovered | it gains no authority from filename, date, or status; continue only after confirming it is non-authoritative and nonconflicting, otherwise hold and reconcile |
| Owner directs a material SPEC change, or accepted scope changes after terminal status | create a new packet and switch/incorporate the SPEC explicitly |
| Source, dependency, environment, SPEC, or artifact changes after validation | hold the affected claim and rerun the checks that depend on the change |
| Accepted packet's SPEC, source, or artifact changes inside its accepted claim boundary | preserve the revision-bound decision history and use a new implementation/revalidation packet |
| Defect or contradictory evidence appears after acceptance | link a finding to the revision-bound decision and create a new bugfix/revalidation packet; do not rewrite acceptance |
| Merge, rebase, cherry-pick, or parallel-worktree integration | reconcile state/records; validate the integrated tree and final artifact |
| Crash, context loss, or stale handoff | recover from state and authorities; never infer currentness from filename or time |
| Result from a background job owned by the same unfinished packet | route through Plan/Route; reuse only when identity, acceptance, and gates still match |
| Late external/hardware/production evidence for terminal or changed scope | preserve history or create a named revalidation packet; never rewrite acceptance |
| Flaky, retried, skipped, partial, or degraded validation | retain every material limitation and bound the claim |
| New recurring maintenance occurrence | create a new occurrence packet; never let it silently expand an approved queue |
| Growing implementation notes or ledgers | classify by current effect, promote durable facts, then split by topic with a compact router |
| Deferred or closed work | require a reason plus revisit trigger, or closure evidence/owner decision/superseding packet |
| One unit blocked while others are independent | preserve partial evidence; keep noncurrent TODOs/findings in their deferred sections with restore triggers, and move the independent remainder to a new packet |
| Owner requests changes after Report | reuse only a non-terminal packet with unchanged acceptance/gates; otherwise create a new packet |
| Owner revises or revokes a terminal decision | preserve the old decision; create a new decision/revalidation packet and unique revising/superseding record, then update affected current-claim pointers |
| Existing declared gate becomes satisfied | continue the packet if action, conditions, source/artifact identity, and expiry still match; a new boundary/term requires re-planning |
| Validation/tests become weaker or a version lane changes | reassess the proves claim and bind a lane-specific packet/validation |

Before state leaves a terminal packet, one durable owner-decision record must
bind its packet ID, active SPEC path and exact revision, source/artifact
identity, evidence and claim limits, unresolved risk, and final decision.
Unrelated repository edits do not invalidate that history; only changes inside
the accepted claim boundary require a new implementation/revalidation packet.
After split children finish, the original boundary remains unresolved until
aggregate validation and an owner decision close it or an accepted replacement
explicitly retires it.

Not every packet executes every phase. A read-only review may mark Implement as
not applicable; a planning packet may stop before implementation; a blocked
packet may stop before verification; and a no-change review may report without
a write. Skipping a phase is valid only when the report names it, explains why,
and does not claim evidence that the omitted phase would have produced.

## Report

Report findings first, then:

- interpreted intent and active boundary,
- changed files or artifacts,
- validation evidence,
- limits and unverified areas,
- documents actually read or updated,
- owner decision or acceptance needed,
- next action.

If this run confirms repeated pain or one high-risk missing control, record the
finding/evidence and root cause, choose the smallest durable control plus
regression evidence, and later Keep/Refine/Merge/Retire it after field use.
Prefer refining an existing rule, flow, check, or template. Apply it now only
inside the active boundary; otherwise record a bounded follow-up.

Only when another session, tool, person, or machine needs actual continuity,
create a packet-bound handoff and set `current_handoff`. A stop, redirect,
block, or partial result alone does not require one. Link authorities rather
than copying them; clear or replace a stale pointer.

## Owner Gate

Stop before protected actions such as release, migration, destructive changes,
production impact, sensitive-data access, auth, money, security, or risk
acceptance unless a valid owner authorization, including an explicit current
command, covers that exact action and its conditions.

Record a reusable conditional authorization with:

```text
Decision: authorized | revoked | superseded
Revises/supersedes authorizations:
Authorized action:
Packet:
Conditions:
Source/artifact identity:
Expires when:
Evidence required before action:
Owner or decision source:
Decided at:
```

Reuse it only while the action, packet, conditions, source/artifact identity,
and expiry remain unchanged. A changed term or expired condition requires a new
owner decision. A current owner restriction, cancellation, or revocation ends
reuse immediately. Append a revising/superseding record rather than editing
history, and restore the affected gate as unsatisfied before another protected
action.

Markdown guidance and decisions do not technically prevent tools from acting.
Permissions, hooks, sandboxes, protected branches, and service controls provide
enforcement.
