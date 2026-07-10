# Advanced Extensions Playbook

Status: On demand
Trigger: repeated eval loop, harness optimization, self-improving agent loop,
retrieval/memory tuning, scheduled loop, or model-routing experiment

Do not add an advanced control surface because it is interesting. Require:

- a repeated, stable task unit;
- a measurable metric and baseline;
- fixed model/tool and allowed-change surfaces;
- separate search and held-out evaluation sets;
- explicit evidence and owner-acceptance criteria;
- evaluation leakage and private-data review;
- concrete time, token, compute, and retry budgets;
- rollback and stop rules;
- an owner adoption gate.

Mark missing fields as unknown or blocking. Keep advisor approval, worker
completion, evaluator pass, and owner acceptance as separate states. A passing
loop evaluator cannot approve a new scope, release, or destructive action.

Prefer isolated exploration for one-off research, a skill/playbook for repeated
procedure, deterministic validation for required guarantees, and reviewed
project memory for durable decisions. Remove the extension when its maintenance
cost exceeds the measured benefit.
