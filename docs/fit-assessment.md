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
5. Is there release, migration, user data, auth, money, or production risk?

| Yes answers | Recommendation |
|---|---|
| 0 | Use a one-shot prompt. Do not install SDAD files. |
| 1-2 | Use [Mini SDAD](mini-sdad.md). |
| 3 | Use Standard SDAD with core control files. |
| 4-5 | Use Full SDAD with review, ADRs, and risk gates. |

When unsure, choose the smaller scale. Escalate only when repeated pain,
context loss, risk, or multiple sessions appear.

Maintenance cost matters: choose Standard or Full SDAD only when you can keep
`SPEC/SPEC-COMPLETE.md`, `docs/TODO-Open-Items.md`, `review-findings.md`, and
rules/ADRs current at the end of each loop. If that cost is too high, use
[Mini SDAD](mini-sdad.md) or a one-shot prompt.

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

## Score

| Score | Fit | Recommendation |
| --- | --- | --- |
| 0-8 | Low | Use a one-shot prompt or [Mini SDAD](mini-sdad.md). Do not install the full workflow unless the project grows. |
| 9-17 | Medium | Use core control files: `AGENTS.md`, `docs/INDEX.md`, SPEC, TODO, and review findings. |
| 18-24 | High | Use the full SDAD workflow with cross-review, source-of-truth rules, and documentation consistency checks. |
| 25-30 | Very high | Use full SDAD plus ADRs, release gates, anti-pattern review, fit reassessment, and tool adapters. |

## Output Template

```text
Project:
Score:
Fit:
Recommended control files:
Required review roles:
Risk gates needed:
Owner decisions needed before implementation:
Smallest verified first slice:
```

## Reassessment

Re-run this assessment when:

- a project moves from prototype to release,
- multiple AI tools start contributing,
- historical docs begin to conflict,
- production-readiness claims appear,
- the owner feels progress is hard to judge.
