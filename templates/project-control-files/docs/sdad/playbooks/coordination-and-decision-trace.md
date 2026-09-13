# Coordination And Decision Trace Playbook

Status: On demand
Trigger: material decision-impact review; two or more delegated lanes; sibling
result reconciliation; or long-running Rule 5 lifecycle closure
Compatibility: optional SDAD 3.2.2 document profile

This playbook is the operational form of the
**SDAD 3.x Coordination and Decision Trace Profile**. It adds no state field,
schema, Doctor check, service, scheduler, lock, or required command.

## Authority And Limits

Keep the existing authority model:

- intended scope and acceptance criteria live in the active SPEC;
- current and deferred work live in TODO;
- defects, failed checks, unresolved risks, and blocked gates live in findings;
- spec-unstated implementation decisions live in implementation notes;
- durable architecture, policy, security, release, or owner-approved tradeoffs
  live in ADRs;
- evidence and claim status live in their existing ledgers;
- owner authorization or acceptance lives in one durable decision record;
- execution identity and status live only in `sdad-state.yaml`;
- continuity lives in the state-declared current handoff.

Other documents link these authorities by path, heading, or stable ID. They do
not copy mutable facts.

This profile provides procedural review, not executable exclusion. A written
lane, dependency, or terminal result is not a lock, lease, epoch, fencing token,
compare-and-swap operation, automatic dispatch, or integration guarantee.

## Activate And Route

Keep the profile dormant for one agent and one bounded unit or packet unless a
material decision trace is actually needed.

When triggered:

1. confirm that the current packet and acceptance boundary authorize the work;
2. route this playbook and `docs/implementation-notes.md` through
   `sdad-state.yaml#routed_docs` for the affected packet;
3. keep the parent or integration item visible in TODO;
4. declare delegated scope, dependencies, evidence, and stop conditions before
   parallel implementation;
5. remove the optional routes when the trigger ends and reconciliation is
   complete.

A read-only viewer such as SDAD Inspector may display these canonical Markdown
files. It does not become an authority and must not infer dependency
satisfaction, integration, acceptance, or release from their presence.

## Decision Trace

When this profile is active, every material implementation decision records:

- the originating packet and TODO or finding;
- the decision, rationale, and rejected alternatives;
- bounded direct-impact references to work, paths or artifacts, claims or
  evidence, and validation;
- later realization references to changed files and evidence;
- supersession, verification impact, and follow-up.

Use the optional fields in `docs/implementation-notes.md`. Promote durable
architecture or policy to an ADR and leave only a pointer in implementation
notes.

Direct impacts are immediate known effects, not a guessed transitive graph.
`Realized by` is a bounded implementation/evidence reference, not raw reasoning
or a mechanical edit log. A correction creates a superseding record rather than
rewriting historical meaning.

Parallel branches must resolve duplicate `IMPL-NNNN`, ADR, finding, or packet
IDs before merge and update every affected reference. Neither filename order,
date, nor the larger ID selects a current decision. Competing successors for
overlapping scope require explicit reconciliation.

## Delegated TODO Lanes

Represent a delegated unit inside the existing TODO rather than adding Dispatch
or Run entities:

```md
- [ ] [packet:auth-refresh] Refresh-token validation
  - Lane: worker-a
  - Scope: src/auth/**, tests/auth/**
  - Must not edit: src/database/**
  - Depends on: none
  - Decision references: IMPL-0042
  - Required evidence: unit test and integration test
  - Integration target: owner-named current target
  - Terminal result: pending
  - Result evidence: none
```

`Lane` is a human-readable assignment label, not identity or authority. It does
not replace the packet ID. Parallel independent write branches or worktrees
retain distinct child leaf packet IDs under the work-packets playbook; the
parent or an explicit integration packet reconciles them.

Allowed terminal results are:

```text
completed
failed
cancelled
rejected
superseded
```

Apply these rules:

1. Resolve scope overlap before parallel writing, either by removing the
   overlap or naming one integration owner and serialization boundary.
2. A lane may not silently expand its scope.
3. Only `completed` with all required evidence satisfies a dependency.
4. `failed`, `cancelled`, `rejected`, and `superseded` require an explicit
   disposition and do not by themselves satisfy a dependency or acceptance
   criterion.
5. A completed lane is an agent result, not integration, packet completion,
   owner acceptance, or release.
6. Validate the final combined tree, not only each isolated lane.

## Packet Finalization Barrier

> A packet cannot become evidence-ready while any required delegated lane is
> pending, unknown, blocked without disposition, or missing required evidence.

Before packet closure, reconcile:

```md
## Parallel Result Reconciliation

- Required lanes:
- Completed lanes with required evidence:
- Pending or unknown lanes:
- Failed, cancelled, rejected, or superseded lanes and disposition:
- Scope or decision conflicts:
- Combined-tree validation:
- Remaining TODOs or findings:
- Evidence-ready: yes | no
- Owner decision needed:
```

A failed or cancelled required lane remains unresolved until a replacement
completes with evidence or an owner-authorized SPEC/packet change removes the
criterion. Deferring the lane alone cannot close an unchanged acceptance
boundary. An individually green child or lane cannot close its parent.

## Agent-Discovered Input

Discovery does not grant scope. Route it by fact type:

| Discovered condition | Authoritative route |
| --- | --- |
| Clear defect in active scope | Active review finding |
| Work already required by an active acceptance criterion | Active TODO linked to the criterion |
| Improvement outside active scope | Future or deferred TODO candidate |
| Repeated pain or one high-risk missing control | Finding plus Rule 5 candidate |
| Protected, destructive, release, production, security, or policy action | Owner gate or decision candidate |
| Duplicate or semantically equivalent item | Link the existing record |

When a separate candidate block is useful, record only discovery provenance,
observed evidence, possible impact, duplicate search, proposed route, activation
authority, and revisit trigger. Do not implement it until the active packet and
acceptance boundary authorize it.

## Rule 5 Lifecycle

Keep a project-specific rule in its existing human-readable authority. Do not
create a second rule registry for this profile.

```text
Finding
-> root cause
-> smallest durable control
-> regression evidence
-> field use
-> Keep | Refine | Merge | Retire
```

A candidate remains non-normative until routed through the existing owner and
rule authority. Inspector export, a successful regression, or agent preference
does not activate it.

## Result And Claim Vocabulary

Use coordination result labels separately from packet status and claim facts:

| Term | Meaning |
| --- | --- |
| Agent completed | One named lane reports its bounded task finished |
| Integrated locally | The result exists in the named local integration target |
| Evidence-ready | Declared scoped checks passed and limitations are stated |
| Software-verified | Required local software evidence passed |
| Owner-accepted | The owner accepted the named result and claim boundary |
| Released | A named release artifact or tag was actually published |
| Production-ready | Declared production evidence and owner gates completed |
| Insufficient evidence | Available evidence cannot support the requested claim |

`Agent completed`, `Integrated locally`, and `Released` are not new
`active_packet.status` values. Preserve the existing SDAD state vocabulary and
do not collapse any of these meanings into a generic `done`.

## Handoff, Redirect, And Recovery

A handoff may point to active lanes, unresolved results, decision records,
combined-tree validation still required, and the exact restore trigger. It does
not copy full TODO, finding, decision, or evidence records.

After an owner redirect or cancellation, stop affected lanes and treat late
results as stale until the new packet routes and revalidates them. A missing
report remains unknown; silence is not completion. Re-enter through adapter,
state, and INDEX, then reconstruct from current repository authorities.

## Review Checklist

Before reporting the profile evidence-ready, confirm:

1. the profile stayed dormant when its trigger was absent;
2. each material decision has one origin and one authoritative home;
3. lane scopes, dependencies, required evidence, and integration target are
   explicit;
4. only completed lanes with required evidence satisfy dependencies;
5. no required sibling is pending, unknown, or disposed without preserving the
   acceptance boundary;
6. late results, overlapping decisions, and identifier collisions were
   reconciled;
7. combined-tree validation covers the final integration target;
8. out-of-scope discoveries remain candidates;
9. Rule 5 candidates end in a visible Keep, Refine, Merge, or Retire decision
   after field use;
10. evidence-ready, owner acceptance, release, and production claims remain
    distinct.
