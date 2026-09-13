# W0 implementation baseline

Status: isolated local implementation candidate; no release or owner acceptance.

| Layer | Baseline | Reuse decision |
| --- | --- | --- |
| Released SDAD | v3.2.2, `cd1b1ddb3e6bcb19b531034742c7d67b4257768e` | Immutable comparison/runtime; state v2 and Doctor contracts retained |
| Protocol source | HEAD `2cbf36a` plus preserved local candidates | Renderer atomic writes, path/BOM and validator robustness retained as dependency hardening; optional coordination Markdown remains optional |
| Inspector source | HEAD `90bff515237c2353e4a070107815f34c701a0534` plus SI-019/020 local candidates | Existing bounded document reader, path fixes, three-pane UI, source viewer, themes and four-language catalog retained |
| New SDAD 4.0 work | `codex/sdad-4-interaction-mvp` in isolated protocol and Inspector worktrees | W1 execution meaning, W2 optional reporting contract, W3 request view, W4 manual correction roundtrip |

The starting protocol candidate contained 23 modified/untracked files and the
Inspector candidate 12. They were copied into isolated worktrees before new
implementation. This is a candidate selection, not acceptance of the original
dirty changes or a claim that they are in a public release. Source hashes were
recorded and the original candidate files remained unchanged during implementation.
Ignored local Inspector control documents were copied to reconcile SI-021;
runtime and frontend dependencies are reused through local junctions.

The former v4 designs stay retired. No separate Core, graph, forced state-schema
migration, mandatory multi-agent scheduler or new cloud service is introduced.

The software test journey uses an explicitly synthetic settings scenario:
same-browser interpretation -> cross-device correction -> copy -> old response
ignored -> matching response with evidence shown. It tests Inspector behavior,
not an implemented settings-sync product. Actual user burden and productivity
measurement are W5; native packaging and release validation are W7.
