# SDAD Protocol Owner Guide

The owner does not need to memorize protocol vocabulary. The owner sets the
outcome, keeps protected decisions explicit, and accepts or rejects evidence.

## 10-Minute Rollout

1. Send the [Copy-Paste Start Prompt](../README.md#copy-paste-start-prompt).
2. Let the AI inspect the request and repository before asking questions.
3. Review its proposed scale, execution scope, owner gates, and claim boundary.
4. Approve the first `unit` or `packet`, not every micro-task.
5. At the checkpoint, require evidence and limits before acceptance.

The bootstrap prompt is one-time. Later sessions start from the installed
adapter, `sdad-state.yaml`, and `docs/INDEX.md`.

## Fast Control Rules

| Control | Owner question |
|---|---|
| Scale | Which persistent control surface is worth maintaining? |
| Execution scope | May the AI complete this unit or this packet now? |
| Owner gate | Which protected action still requires my decision? |
| Validation contract | What will be checked, and what will it prove? |
| Acceptance | Is the evidence sufficient for me to accept the result? |

Defaults are One-shot for the current request, Mini for a `unit`, Standard for
a `packet`, and Full for a `packet` plus applicable named gates.

## Owner Decisions That Must Stay Explicit

Keep owner control for release, deployment, migration, destructive action,
sensitive data, auth, money, security, rollback, production claims, risk
acceptance, and any scope expansion beyond the active boundary.

Scale and execution scope never grant these actions. Evidence-ready also does
not mean owner-accepted.

## First Prompt For Actual Work

```text
Inspect the repository and propose the smallest SDAD scale, a unit or packet
boundary, validation evidence, and applicable owner gates. Ask one question only
if an unresolved fact materially changes those controls. Then work to
evidence-ready within the approved boundary and stop before any unapproved gate.
```

## Conditional Authorization

Avoid repeated approval by recording a bounded decision:

```text
Decision:
Authorized action:
Packet:
Conditions:
Expires when:
Evidence required before action:
```

For example, authorization to push a branch can remain valid for one packet if
the local full gate passes and source does not change afterward. A source,
packet, action, condition, or expiry change invalidates that authorization.

## What To Ask At The Checkpoint

- What changed?
- Which validation commands ran, and what did they prove?
- What remains unverified or outside the claim?
- Which routed documents were actually read or updated?
- Are TODOs, findings, validation, and handoff bound to this packet?
- Is this evidence-ready, and what owner acceptance or gate remains?

Doctor green is structural evidence only. A task benchmark proves that task
only. Require a controlled comparison before accepting a claim that a process
or protocol version is more effective.

## Low-Friction Owner Rules

- Approve packet boundaries, not implementation micro-steps.
- Let the AI infer first; ask only one material question at a time.
- Reuse a valid conditional authorization until its recorded expiry.
- Treat `routed_docs` as selectable routes, never a full-read requirement.
- Keep one fact in one authoritative home; handoffs link rather than copy.
- Use technical enforcement for permissions. Markdown is guidance and record,
  not a sandbox.

## Adoption Health Check

A healthy project can answer from adapter -> state -> INDEX:

- the active packet and next action,
- the validation contract and claim limit,
- the applicable owner gate,
- which document should be read now,
- which documents should not be loaded,
- whether the result is evidence-ready or owner-accepted.

Warning signs are stale handoffs, broad full-read instructions, validation that
belongs to another packet, repeated facts across files, expired authorization,
or effectiveness claims based only on Doctor/unit-test output.

## Migrating From SDAD 3.1

Legacy autonomy levels, operating intensity, Q5 wording, owner checkpoints,
recovery modes, and `save-state.md` are state-v1 migration vocabulary. Do not
lead new users with them. Show a read-only preview, preserve v1 behavior until
the owner approves migration, and write only state-v2 controls afterward.
