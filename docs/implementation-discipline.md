# Implementation Discipline

Status: Active reference
Scope: Coding behavior inside an approved SDAD work packet

SDAD is the project control layer. Implementation discipline is the lower-level
coding behavior that keeps AI autonomy from becoming messy.

This page adapts compatible lessons from
[forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills)
and Andrej Karpathy's public observations about LLM coding pitfalls. Keep this
as a guardrail inside SDAD, not as a replacement for SPEC, evidence, review, or
owner checkpoints.

## 1. Surface Assumptions

Before coding, state the assumptions that affect scope, design, risk, or
verification.

Use the autonomy model:

- local implementation assumption with low risk: state it, proceed, verify, and
  report it in the checkpoint;
- product, risk, release, data, auth, money, destructive, or policy assumption:
  stop and ask the owner;
- conflicting evidence: stop and show the conflict.

The goal is not to ask more often. The goal is to avoid silent guessing.

## 2. Prefer The Smallest Working Design

Implement the minimum code that satisfies the active SPEC and evidence criteria.

Avoid:

- speculative features,
- single-use abstractions,
- configurability nobody asked for,
- broad future-proofing,
- error handling for impossible states that are outside the accepted scope.

If the solution became much larger than the problem, pause locally and simplify
before handoff.

## 3. Make Surgical Changes

Every changed line should trace to the work packet, the active SPEC, a review
finding, or required cleanup caused by the current edit.

Do:

- match the existing style,
- touch only the files needed for the packet,
- remove imports, variables, or files made unused by your own change,
- mention unrelated dead code or cleanup opportunities instead of editing them.

Do not:

- refactor adjacent code just because it looks imperfect,
- reformat files unrelated to the change,
- delete pre-existing dead code unless asked,
- rewrite comments or docs that you did not need to touch.

## 4. Make Goals Verifiable

Turn requested work into success criteria before implementation.

Examples:

- bugfix: reproduce or describe the failing behavior, fix it, then verify it no
  longer happens;
- validation change: define valid and invalid cases, then test or manually check
  them;
- refactor: show that behavior stayed the same before and after;
- docs or prompt change: show which workflow confusion the change prevents.

For multi-step packets, use a short plan where each step has a matching check.
This lets the AI continue autonomously inside the packet without asking for
permission after each small task.

## Working Signals

This discipline is working when:

- diffs contain fewer unrelated changes,
- simple tasks stay simple,
- assumptions are visible before they become bugs,
- verification maps to the stated goal,
- owner checkpoints receive evidence instead of apology-driven rewrites.
