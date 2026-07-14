# Project Name

One paragraph explaining what this project is and who it is for.

## Development Workflow

This project uses SDAD Protocol (SPEC-Directed AI Development), a
repository-local operating protocol that leaves the implementation method open.

- The owner controls direction and final acceptance.
- AI agents use Plan -> Route -> Implement -> Verify -> Report inside the
  declared unit or packet.
- Evidence-ready and owner-accepted are separate checkpoints.
- Claims require code, tests, docs, artifacts, or runtime evidence at the tier
  named by the active packet.

The Core 5:

1. Current beats historical.
2. Evidence beats confidence.
3. Active beats interesting.
4. Owner decision beats AI momentum.
5. Repeated pain becomes a rule.

Compression first. Gates stay real.

For repeated pain or one high-risk control failure, record the root cause,
choose the smallest durable control plus regression evidence, and later
Keep/Refine/Merge/Retire it; refine existing controls before adding rules.

## Start Here

Use the compact control plane:

1. The installed tool adapter provides the always-loaded safety and execution
   kernel at its native path.
2. `sdad-state.yaml` names the active packet, execution scope, owner gates,
   validation contract, and eligible routed documents.
3. `docs/INDEX.md` maps the current trigger to one policy section or playbook.
4. Inspect current source/tests; current intent selects only the needed routed
   path, heading, active section, or targeted match.

Route membership permits selection; it never means a full-file read of every
route. Do not read the complete rulebook, archives, old handoffs, or optional
evidence files by default.
A current owner-named input may still be inspected within the request when a
stale route omits it; if adopted, reconcile authority and routes before stateful
implementation.

## Load On Demand

- large/private input: `docs/sdad/playbooks/context-and-data.md`;
- scale, execution scope, packet, or delegation:
  `docs/sdad/playbooks/work-packets.md`;
- owner gates, claims, parity, or release:
  `docs/sdad/playbooks/evidence-and-risk-gates.md`;
- docs/state/handoff: `docs/sdad/playbooks/documentation-and-handoff.md`;
- adaptive-rule portability or harness/eval/memory loops:
  `docs/sdad/playbooks/advanced-extensions.md`;
- durable policy: the relevant heading in
  `docs/Repository-Operating-Rules.md`.

Spec-unstated implementation decisions go in `docs/implementation-notes.md`.
Hard-to-reverse surprising tradeoffs use a numbered ADR.

## Optional Evidence

Optional product evidence files are create-on-demand. Do not treat a missing
optional evidence file as a setup failure unless the project is making a claim
that needs that evidence boundary.

Use `docs/evidence-matrix.md`, `docs/claim-registry.md`,
`docs/artifact-contracts.md`, `docs/work-packet-state.md`, and
`docs/remote-evidence-import.md` only when an active claim needs them.

Small Project Compression Rule: if the current packet has one active slice, no
owner gate changed, no durable finding or spec-unstated decision must survive,
no handoff is expected, and evidence fits in a short summary, do not create extra
control files just to look complete.

When a real cross-session checkpoint is needed, create a compact handoff and
declare its path once as `current_handoff` in `sdad-state.yaml`. Remove or
replace that pointer on a packet switch.

For stateful work, `sdad-state.yaml#active_spec` is the single normative SPEC
entrypoint. Treat `SPEC-COMPLETE.md` as an integrated baseline. A SPEC supplied
as current requirements is a change request unless the owner limits it to review/draft/reference;
reconcile it before affected work. A merely discovered file remains a proposal
only when non-authoritative and nonconflicting. A material post-acceptance
change uses a new packet ID and fresh validation. When ledgers or implementation notes grow, promote each fact to its
authoritative home, split remaining current records by topic, and keep the main
file as a compact router.
