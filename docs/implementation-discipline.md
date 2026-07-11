# Implementation Discipline

Status: Active reference
Scope: Coding behavior inside an approved SDAD work packet

SDAD is the project control layer. Implementation discipline is the lower-level
coding behavior that keeps bounded AI execution from becoming messy.

This page adapts compatible lessons from
[multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)
and Andrej Karpathy's public observations about LLM coding pitfalls. It also
adapts compatible clarification and documentation patterns from
[mattpocock/skills](https://github.com/mattpocock/skills). Keep this as a
guardrail inside SDAD, not as a replacement for SPEC, evidence, review, or owner
decisions.

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

## 2. Run A Clarification Checkpoint When The Plan Is Fuzzy

Use a clarification checkpoint when the work packet has ambiguous scope,
overloaded terms, a hard-to-reverse choice, unclear evidence, or a likely owner
tradeoff.

Before asking the owner, inspect the current code, tests, active docs, SPEC, and
review findings. If the repository already answers the question, use that answer
and cite the evidence in the checkpoint.

When a question remains:

- ask only the next blocking question instead of dumping a long interview,
- include the AI's recommended answer,
- state why the question matters,
- state what will change if the owner chooses a different answer.

If the answer is a low-risk local implementation assumption inside the approved
packet, state the assumption and proceed. If it changes product behavior, risk,
scope, release posture, data/auth/money/security, or an owner-controlled
tradeoff, stop for the owner.

If the ambiguity is terminology, propose one canonical term and one short
definition. Keep terminology in active docs or SPEC when it affects execution.
For projects with repeated domain-language confusion, create a small optional
`docs/domain-language.md` routed from `docs/INDEX.md`; keep it glossary-only, not
an implementation log.

Resolved checkpoint outcomes must be routed:

- SPEC or active docs for behavior and source-of-truth changes,
- `docs/implementation-notes.md` for spec-unstated implementation choices,
- ADRs for durable hard-to-reverse decisions,
- `docs/TODO-Open-Items.md` or `review-findings.md` for follow-up work or risk,
- handoff notes when the session must restart later.

## 3. Prefer The Smallest Working Design

Implement the minimum code that satisfies the active SPEC and evidence criteria.

Avoid:

- speculative features,
- single-use abstractions,
- configurability nobody asked for,
- broad future-proofing,
- error handling for impossible states that are outside the accepted scope.

If the solution became much larger than the problem, pause locally and simplify
before handoff.

## 4. Make Surgical Changes

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

## 5. Make Goals Verifiable

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

## 6. Preserve Implementation Memory

When the active SPEC does not decide a necessary implementation choice, record
the decision in [implementation-notes.md](implementation-notes.md).

Record assumptions, SPEC gaps, implementation changes, compromises, rejected
alternatives, owner-relevant tradeoffs, follow-up work, and verification impact.
Do not record raw internal reasoning, every mechanical edit, or large logs.

## Working Signals

This discipline is working when:

- diffs contain fewer unrelated changes,
- simple tasks stay simple,
- assumptions are visible before they become bugs,
- plan ambiguity is resolved before coding or explicitly escalated,
- project terminology stops shifting between sessions,
- verification maps to the stated goal,
- spec-unstated decisions are available to the next session,
- owner gates and acceptance decisions receive evidence instead of apology-driven rewrites.
