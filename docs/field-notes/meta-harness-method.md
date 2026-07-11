# Meta-Harness Method

Status: Active reference
Scope: Harness optimization, retrieval/memory/context construction, tool-use
scaffolds, and repeated evaluation loops

This note adapts the Meta-Harness research pattern to SDAD. Meta-Harness treats
a harness as the code around a fixed base model that decides what information to
store, retrieve, and present while the model works. SDAD uses that idea only as
an advanced extension: a governed way to improve the control layer around an AI
system when there is a repeated task, measurable evaluation, and owner-reviewed
adoption gate.

References:

- https://github.com/stanford-iris-lab/meta-harness
- https://arxiv.org/abs/2603.28052

## SDAD Translation

Use this pattern when the thing being improved is not the product code itself,
but the surrounding harness:

- retrieval policy,
- memory policy,
- context selection,
- tool-use scaffold,
- prompt or review rule set,
- run-history and trace inspection,
- planning or decomposition wrapper.

Do not use this as the default SDAD loop. Normal SDAD improves a project through
SPECs, work packets, evidence, review, and owner decisions. Harness optimization
is a higher-cost extension that searches over candidate harnesses and evaluates
their behavior.

## Fit Gate

Before starting harness optimization, every field below must be answered,
marked `unknown`, or marked `blocking`:

| Field | Required Answer |
|---|---|
| Task unit | One repeated evaluation unit, such as one ticket, task, episode, document, or benchmark case |
| Fixed base | Model, tool surface, data access, and product code that will not change during the search |
| Harness boundary | What candidate harnesses may change, and what is explicitly out of scope |
| Harness interface | The API, file shape, prompt contract, or runner contract every candidate must satisfy |
| Search set | Cases used to compare candidate harnesses during optimization |
| Held-out set | Cases reserved for owner acceptance or final evidence, or the reason none exists |
| Metrics | Primary success metric plus secondary cost, latency, timeout, quality, or safety metrics |
| Leakage risk | How search evidence could contaminate held-out acceptance evidence |
| Baselines | Obvious hand-written baseline and strongest current harness |
| Offline experience | Prior traces, reports, docs, or failure notes that may inform candidates |
| Online experience | Candidate traces, metadata, scores, logs, and artifacts to preserve |
| Budget | Candidate count, wall-clock time, token/API spend, evaluation runs, or owner review time |
| Adoption gate | Owner acceptance required before any discovered harness becomes active |

## Eleven Harness Surfaces

When a project says "the AI harness is bad", classify the pain before changing
the system:

1. Task specification: the task unit and success target are unclear.
2. Context selection: the harness retrieves or shows the wrong information.
3. Tool access: tools are missing, unsafe, noisy, or overpowered.
4. Project memory: prior decisions, traces, or examples are unavailable.
5. Work state: candidate state, TODOs, failures, or open assumptions are hidden.
6. Observability: scores, traces, intermediate decisions, or costs are not
   inspectable.
7. Failure analysis: recurring errors are not converted into candidate changes.
8. Verification: search and held-out evaluation are missing or mixed together.
9. Permissions: the harness can change behavior without a clear owner gate.
10. Entropy reduction: each iteration adds more rules without simplifying the
    control layer.
11. Intervention record: human changes, overrides, and adoption decisions are
    not recorded.

Use the smallest surface that explains the failure. Do not widen the search to
all prompts, tools, memory, and code unless the owner explicitly approves the
expanded budget and risk.

## Required SDAD Artifacts

For a small exploratory pass, record the fit gate in a work packet or handoff.
For a durable harness optimization track, create one maintained control surface,
usually `docs/harness-optimization.md`, with:

- task unit and harness boundary,
- fixed base model and tool surface,
- allowed changes and out-of-scope changes,
- search set and held-out set,
- metrics and leakage risks,
- baseline harnesses,
- candidate log and result table,
- online trace and artifact retention rule,
- concrete budget,
- owner adoption checkpoint.

Link candidate traces and raw logs by path. Do not paste large traces into
active docs. Use bounded reads for archives and preserve only the current
decision summary in handoffs.

## Evidence Boundary

Search evidence can make a candidate harness evidence-ready. It does not make
the harness owner-accepted.

Owner acceptance requires a named checkpoint that reviews:

- the search/held-out split,
- leakage risk,
- baseline comparison,
- budget used,
- changed behavior,
- regressions and known failures,
- adoption plan and rollback path.

If the split is weak, the budget was exceeded, or the candidate changes product,
security, data, money, release, or owner-policy behavior, keep the candidate
blocked or qualified until the owner accepts the risk.

## Stop Rules

Stop the harness optimization loop when:

- the concrete budget is exhausted,
- the held-out set is contaminated,
- the candidate requires changing the fixed base model or tool surface,
- the evaluation metric no longer reflects owner value,
- trace volume makes active docs unreadable,
- the winning candidate is not meaningfully better than the baseline,
- adoption would change a protected-action owner gate without owner review.

When stopped, record the best candidate, failed candidates, budget used, and the
next owner decision. Do not silently convert "promising" into "adopted".
