# Autonomy Levels

Status: Active reference
Scope: How much an AI agent may do before asking the owner again

SPEC-Driven AI Development should reduce chaos, not create approval fatigue.
Owner control does not mean the owner must approve every edit, TODO, or small
task. It means the owner defines the boundary, risk posture, and stop
conditions, then reviews evidence at meaningful checkpoints.

## Evidence-Ready Is Not Owner-Accepted

Use two states:

- `AI-complete / evidence-ready`: the agent believes the work is ready for
  review and shows changed files, checks, docs updated or checked, limitations,
  and open risks.
- `Owner-accepted`: the owner has reviewed the checkpoint and accepted,
  rejected, revised, or deferred the result.

An agent may continue from one evidence-ready unit to the next when both units
are inside an approved work packet. It must not call the whole packet "done"
until the owner checkpoint has happened or the owner has explicitly delegated
that acceptance policy.

## Work Packet

A work packet is a bounded container for one or more review-worthy development
units.

Define it before implementation:

```text
Work packet:
- Goal:
- Autonomy level:
- Allowed scope and files:
- Review-worthy units included:
- Non-goals:
- Stop conditions:
- Evidence required:
- Checkpoint cadence:
```

The packet should be large enough that owner review is meaningful, but small
enough that evidence can be checked without re-reading the whole project.

## Levels

| Level | Name | Behavior | Good for |
|---|---|---|---|
| 0 | Ask-first | Ask before each meaningful step. | New, ambiguous, or risky setup. |
| 1 | Unit autonomy | Complete one review-worthy unit, then hand off evidence. | Mini SDAD and small fixes. |
| 2 | Work-packet autonomy | Complete multiple related units inside one approved packet, then checkpoint. | Default for Standard SDAD. |
| 3 | Session autonomy | Work until the session goal, time box, or stop condition is reached. | Low-risk docs, tests, cleanup, or implementation passes. |
| 4 | Release-gated autonomy | Prepare release or production work, but owner gates release, migration, destructive actions, and risk acceptance. | Full SDAD and Q5 risk projects. |

Recommended defaults:

- One-shot prompt: no persistent autonomy contract.
- Mini SDAD: Level 1 by default; Level 2 only if the owner names a packet.
- Standard SDAD: Level 2 by default.
- Full SDAD or Q5 risk: Level 2 for implementation, with Level 4 gates for
  release, migration, destructive actions, data/auth/money/security decisions,
  rollback, and production claims.

## Stop Conditions

At any level above 0, stop and ask the owner only when:

- scope would expand beyond the approved packet,
- Q5 risk, release posture, data, auth, money, migration, security, or
  destructive action changes,
- an owner-controlled product, policy, budget, or tradeoff decision is required,
- verification is blocked or impossible,
- current evidence conflicts with the requested plan,
- the next step would overwrite or discard existing work without owner approval.

Everything else should be handled as "report later with evidence", not "ask now
for permission".

## Checkpoint Summary

At the end of a work packet or session, report:

- autonomy level used,
- work packet completed,
- evidence-ready units,
- changed files,
- tests, builds, lint, or manual checks run,
- docs and control files checked or updated,
- open findings and remaining risks,
- partial, skipped, degraded, or unverified behavior,
- owner decisions needed now,
- next proposed work packet.

For Standard and Full SDAD, update control files at the packet or handoff
boundary. Do not stop after every micro-task just to update documents, but do not
leave stale control files across a handoff.
