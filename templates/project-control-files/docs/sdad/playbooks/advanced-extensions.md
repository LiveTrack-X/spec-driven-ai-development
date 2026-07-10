# Advanced Extensions Playbook

Status: On demand
Trigger: repeated eval loop, harness optimization, self-improving agent loop,
retrieval/memory tuning, scheduled loop, or model-routing experiment

Do not add an advanced control surface because it is interesting. Require:

- a representative task and environment plus a measurable baseline;
- deterministic outcome checks where possible and a fixed model/tool setup;
- separate regression and capability evaluation;
- held-out or fresh tasks for public comparative claims;
- repeated runs for nondeterministic workflows;
- human-calibrated semantic graders when deterministic checks are insufficient;
- final-answer completeness in addition to tool-trace correctness;
- separate evidence-ready and owner acceptance criteria;
- evaluation leakage and private-data controls;
- rollback and stop rules plus an owner adoption gate.

Apply a quality-first budget: meet the quality and evidence bar before comparing
time, tokens, latency, retries, review burden, compute, or cost. Record those
budgets, the rollback trigger, and the owner-controlled stop condition.

Mark missing fields as unknown or blocking. Keep advisor approval, worker
completion, evaluator pass, and owner acceptance as separate states. A passing
loop evaluator cannot approve a new scope, release, or destructive action.

Prefer isolated exploration for one-off research, a skill/playbook for repeated
procedure, deterministic validation for required guarantees, and reviewed
project memory for durable decisions. Remove the extension when its maintenance
cost exceeds the measured benefit.
