# SDAD Evidence Review Prompt

Review this SDAD Protocol packet as an independent reviewer. Read the installed
adapter, `sdad-state.yaml`, and `docs/INDEX.md` first; inspect current source and
tests; then select only the routed paths, headings, active sections, or targeted
matches required by the review. Do not read every `routed_docs` member.

Context Stability applies before review inputs. Use bounded reads above 50 KB,
run a context-stability check above 200 KB, and do no full startup read above 1
MB. Treat private data as an authorization boundary regardless of size. Prefer
metadata, schema, sample, targeted search, redaction, and explicit excludes.

## Establish The Review Boundary

Establish these before reviewing, but place them after findings in the Evidence
or Unverified Areas output sections:

- state schema, scale, and `execution_scope`;
- exact active packet marker and objective;
- validation contract owner (`validation_for`) and bounded claims;
- applicable owner gates and any reusable conditional authorization;
- routed documents actually read;
- excluded or unverified areas.

Do not assume worker context, prior chat, provider task/checkpoint state, or an
old handoff is current. If state declares `current_handoff`, read it only when
continuity affects this review and verify its first Session Identity marker
matches the packet.

## Review For

1. Correctness defects, regressions, unsafe behavior, and unmet acceptance.
2. Validation that does not establish its stated `proves` claim or belongs to a
   different packet.
3. Active TODO/finding markers for another packet, or terminal state with open
   current records.
4. Source, tests, SPEC, state, INDEX, ledger, handoff, and public-doc drift.
5. Unrecorded spec-unstated implementation decisions: small choices belong in
   `docs/implementation-notes.md`; hard-to-reverse decisions belong in ADRs.
6. Evidence overclaim, skipped/partial checks, weak artifact verification, or
   owner acceptance inferred from evidence-ready status.
7. Protected actions without a current owner gate or authorization, and
   authorization reused after expiry, failed conditions, missing required
   evidence, or relevant source change.
8. Documentation record audit gaps: change type, routed surfaces, docs changed,
   docs checked with no update needed, and validation commands run.
9. Context, secret, private-data, generated-artifact, archive, or log handling
   that exceeds its declared authorization or bounded-read need.
10. SPEC lineage drift: more than one claimed normative entrypoint, an
    additional/conflicting SPEC used without explicit incorporation or pointer
    switch, accepted history rewritten, or a material terminal-state change
    kept under a reused packet ID.
11. Lifecycle laundering: unresolved text moved to closed/history without
    evidence, owner decision, or a named superseding packet; deferral without a
    reason and revisit trigger; implementation notes split by age while current
    effects or promoted facts remain duplicated.
12. Stale evidence after source, SPEC, dependency, environment, artifact,
    authorization, merge, rebase, or cherry-pick changes. Integration and
    release claims require validation on the final tree and artifact.

Markdown records guidance/authority but does not technically block tools.
Doctor, tests, and CI are deterministic validation; permissions, hooks,
sandboxing, deny rules, branch protection, and release/deploy controls are
technical enforcement; authorization and acceptance are owner decisions. Do
not report one layer as proof of another.

## Decision And Continuity Rules

Use one authoritative home per fact:

- intended scope/behavior/acceptance criteria -> state-declared `active_spec`;
- observed behavior -> current source/tests/runtime/reproducible commands;
- small spec-unstated implementation decision -> implementation notes;
- hard-to-reverse architecture decision -> ADR;
- unresolved work -> TODO or finding;
- owner authorization/acceptance -> one authoritative owner-decision record;
- evidence/claim status -> evidence or claim ledger pointing to that decision;
- current execution -> `sdad-state.yaml`;
- cross-session recovery links/results -> current handoff.

Treat `SPEC-COMPLETE.md` as an integrated baseline, not immutable or
automatically active. Another SPEC is a proposal unless the active entrypoint
incorporates its exact scope or a packet transaction switches the pointer.
`active_packet.status` is the current dominant checkpoint, not a cumulative
history. Review a skipped loop phase as N/A only when its omission and resulting
claim boundary are explicit.

Handoff-only and state-v1 save-state-only decisions are continuity hints until
promoted to their correct authority. A new state-v2 project does not use
`save-state.md` as current state or handoff authority.

## Required Output

Use findings-first output in this exact order:

1. **Critical/Important findings** — severity, file/line, concrete evidence,
   impact, and smallest corrective action.
2. **Evidence** — commands/checks observed, result, and bounded claim supported.
3. **Compatibility regressions** — especially state-v1 behavior and public
   wire formats; say “none found” when appropriate.
4. **Documentation/state drift** — state/INDEX/validation/ledger/handoff and
   one-fact-one-home issues.
5. **Unverified areas** — skipped, blocked, unavailable, or out-of-scope checks.
6. **No-finding statement** — only when no Critical or Important finding remains.

Keep the internal checklist internal. Do not pad the output with a narration of
every review step. Evidence-ready remains distinct from owner-accepted.
