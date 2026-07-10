# Fit Assessment

Status: Active reference
Scope: Decide whether SPEC-driven AI development is appropriate for a project

Use this assessment before bootstrapping a new project. Score each question:

- `0`: no / not relevant
- `1`: somewhat / likely soon
- `2`: yes / already happening

## 30-Second Scale Gate

Use this quick gate before the full assessment:

1. Will this take more than one AI session?
2. Will you come back to this project later?
3. Does "done" need evidence beyond "AI said so"?
4. Will multiple AI tools or reviewers be involved?
5. Is there release, migration, real user data, auth, money, security, rollback,
   destructive action, or production risk?

Then check the product evidence flag:

- Will product, hardware, compatibility, packaging, remote tester, external lab,
  or release claims need evidence stronger than local software tests?

Override rules beat raw yes-counts:

| Trigger | Recommendation |
|---|---|
| 0 yes | Use a one-shot prompt. Do not install SDAD files. |
| 1-2 yes from Q1-Q3 only, with Q4=no and Q5=no | Use [Mini SDAD](mini-sdad.md). |
| Q4=yes or 3 yes total | Use Standard SDAD with core control files. |
| Q5=yes, but the packet only inspects, documents, or tests the risk area | Use Standard SDAD minimum, even if it is the only yes. |
| Q5=yes and the packet changes, accepts, or executes the gate | Use Full SDAD with review, conditional ADRs, and risk gates. |
| 4-5 yes | Use Full SDAD with review, conditional ADRs, and active risk gates. |

When unsure, choose the smaller scale only if no Q5 gate is active. Escalate
when repeated pain, context loss, risk, or multiple sessions appear.

A yes to the product evidence flag is not automatically Full SDAD, but it does
trigger the relevant product evidence templates. Use Standard SDAD minimum when
those templates must persist across sessions. Changing, accepting, or executing
a Q5 release, production, user-data, auth, money, migration,
destructive-action, or rollback gate still requires Full SDAD.

Maintenance cost matters: choose Standard or Full SDAD only when you can keep
`SPEC/SPEC-COMPLETE.md`, `docs/TODO-Open-Items.md`, `review-findings.md`, and
rules/ADRs current at the end of each loop. If the project uses `save-state.md`,
it must also be updated when sessions pause, handoff is expected, direction
changes, blocked/partial/unverified state remains, or context would be expensive
to reconstruct. If that cost is too high, use [Mini SDAD](mini-sdad.md) or a
one-shot prompt.

## Advanced Extension Fit Gate

Advanced SDAD extensions are optional. They include harness optimization,
self-improving agent loops, repeated evaluation automation, retrieval/memory
tuning, or any workflow that searches over prompts, tools, context construction,
review rules, or agent scaffolds.

Repository control surfaces are usually not an advanced extension by
themselves. Keep them lightweight: always-loaded guidance, routed rules,
on-demand procedures, isolated exploration, enforced guarantees, and reviewed
memory. Escalate to the advanced extension gate only when the project starts
searching over or optimizing those surfaces with repeated evaluation.

Cost-aware agent routing is also usually a normal SDAD structure pattern:
choose lean execution, advisor checkpoints, orchestrator-worker packets, or
bounded loops by difficulty, evidence need, budget, and owner risk. Escalate to
the advanced extension gate only when the project searches over routing policies, models, prompts, evaluators, or loop strategies with repeated evaluation.

Do not enable an advanced extension unless the fit gate is explicit:

- repeated task unit exists,
- measurable success metric exists,
- fixed model and tool surface are named,
- allowed changes and out-of-scope changes are bounded,
- harness interface or candidate contract is named when optimizing a harness,
- search set, held-out set, and baseline harness are named when repeated
  evaluation is used,
- offline traces and online candidate traces are either available or explicitly
  marked absent,
- search evidence is separate from owner acceptance evidence when possible,
- held-out acceptance set exists, or its absence is marked as a risk,
- evaluation leakage risk is named,
- concrete budget is stated in time, candidate count, evaluation runs,
  token/API cost, or owner review time,
- owner adoption gate exists before any discovered change becomes accepted.

Each required field must be answered, marked `unknown`, or marked `blocking`.
Do not silently turn an unknown into an implementation assumption.

If this gate is not satisfied, keep the work inside normal SDAD planning,
manual evaluation, or a smaller work packet. The extension may still be recorded
as a future idea, but it should not become active implementation.

For harness optimization, use
[field-notes/meta-harness-method.md](field-notes/meta-harness-method.md) as the
reference pattern. Treat discovered prompts, retrieval policies, memory
policies, context selectors, tool scaffolds, or review rules as evidence-ready
candidates until the owner accepts the split, leakage risk, budget result,
changed behavior, and adoption plan.

For repository-structure hardening without harness search, use
[field-notes/repository-control-surface-method.md](field-notes/repository-control-surface-method.md).
For advisor, worker, and loop routing without harness search, use
[field-notes/cost-aware-agent-routing-method.md](field-notes/cost-aware-agent-routing-method.md).

## Questions

1. Will more than one AI session, model, or tool work on the project?
2. Does the owner need to supervise direction without writing most code directly?
3. Will the project have active SPECs, historical SPECs, product notes, or archived plans?
4. Is there a risk that old plans could override current code or current decisions?
5. Are docs likely to grow enough that a routing index becomes necessary?
6. Do bugs or review findings need to survive across sessions?
7. Will completion need evidence beyond "the AI says it is done"?
8. Are there security, data loss, migration, tenant, backup, or destructive-action risks?
9. Will the project need release, deployment, rollback, packaging, or production-readiness gates?
10. Are there stable, beta, rewrite, migration, or platform lanes?
11. Will manual or environment-specific verification be required?
12. Are future ideas likely to be tempting but not immediately active?
13. Does the owner want progress reported by scope rather than vague global percent?
14. Would a future maintainer need to know why decisions were made?
15. Has repeated project pain already happened and should become durable rules?
16. Do fuzzy plans or overloaded domain terms repeatedly cause rework or owner
    clarification?
17. Will product, hardware, compatibility, packaging, remote tester, external
    lab, or release claims need evidence stronger than local software tests?

Question 17 is also a routing flag. Even at a lower score, a yes means the
output should name which product evidence templates are needed and why.

## Score

| Score | Fit | Recommendation |
| --- | --- | --- |
| 0-8 | Low | Use a one-shot prompt or [Mini SDAD](mini-sdad.md). Do not install the full workflow unless the project grows. |
| 9-18 | Medium | Use the compact core: one adapter, `sdad-state.yaml`, routing-only `docs/INDEX.md`, SPEC, TODO, findings, and implementation notes when SPEC gaps affect implementation. |
| 19-25 | High | Use the full SDAD workflow with cross-review, source-of-truth rules, and documentation consistency checks. |
| 26-34 | Very high | Use full SDAD plus ADRs, release gates, anti-pattern review, fit reassessment, product evidence templates when needed, and tool adapters. |

## Output Template

```text
Project:
Score:
Fit:
Recommended control files:
Required clarification checkpoints or glossary route:
Required review roles:
Risk gates needed:
Advanced extension fit gate needed:
Advanced extension unknowns/blockers:
Owner decisions needed before implementation:
Recommended autonomy level:
First work packet:
Review-worthy units inside packet:
Implementation discipline risks:
Implementation notes needed:
Product evidence templates needed:
```

## Reassessment

Re-run this assessment when:

- a project moves from prototype to release,
- multiple AI tools start contributing,
- historical docs begin to conflict,
- production-readiness claims appear,
- the owner feels progress is hard to judge.
