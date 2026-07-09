# Cost-Aware Agent Routing Method

Status: Active reference
Scope: Model/tool routing, advisor checkpoints, orchestrator-worker packets, and
bounded agent loops

This note adapts cost-saving multi-agent and loop practices into SDAD. The
useful idea is not that one named model or benchmark ratio should become a
standard. The useful idea is that an AI control layer can route work by
difficulty, cost, latency, evidence need, and owner risk.

Use this pattern when a project is spending too much on high-capability agents,
under-reviewing hard decisions, asking the owner too often, or letting
scheduled/proactive loops run without clear evidence boundaries.

References:

- https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool
- https://platform.claude.com/docs/en/managed-agents/multi-agent
- https://code.claude.com/docs/en/goal
- https://code.claude.com/docs/en/scheduled-tasks
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5

## SDAD Translation

Cost-aware routing is a control structure, not a completion rule.

SDAD uses the smallest agent structure that can protect the packet:

- lean execution contract for ordinary work,
- Executor-Advisor when one agent can execute but needs occasional stronger
  judgment,
- Orchestrator-Worker when independent units can run in parallel or require
  specialized context,
- Loop Engineering when a task should repeat until a condition, schedule, or
  event is reached.

Do not treat a cheaper route as weaker governance. The route is acceptable only
when the evidence boundary, stop rule, and owner gate remain explicit.

## Lean Execution Contract

Use this as the default behavior before adding agents or loops:

1. Inspect current repository evidence first. When there is enough information
   to act, act.
2. Use the simplest design that solves the current packet. Avoid unrelated
   refactors, speculative abstractions, and future-proofing.
3. Report only claims supported by this run's evidence. Label failed,
   unverified, skipped, or uncertain work plainly.
4. Pause only for destructive action, real scope change, owner-controlled
   tradeoff, blocked verification, or information only the owner can provide.
5. Lead with the outcome; put supporting detail after the result.

This is a prompt-level execution contract. It does not replace tests, review,
or owner acceptance.

Do not ask an agent to reproduce hidden reasoning or internal chain-of-thought.
Ask for decisions, evidence, assumptions, alternatives rejected when relevant,
and verification impact.

## Executor-Advisor

Use Executor-Advisor when one executor can do most of the work, but hard
judgment should be escalated sparingly.

Good advisor triggers:

- before committing to an approach on a high-risk or ambiguous packet,
- when repeated errors suggest the current approach is wrong,
- when evidence conflicts with the plan,
- before declaring evidence-ready on a complex packet,
- when a cheaper or narrower executor is likely sufficient for implementation
  but not for architecture, safety, or acceptance-risk judgment.

Advisor output is not owner acceptance. Treat it as review evidence. If the
advisor changes scope, risk, architecture, release posture, data boundary, or
owner tradeoff, route the decision to the owner checkpoint or an ADR instead of
letting the executor silently adopt it.

## Orchestrator-Worker

Use Orchestrator-Worker when the work can be split into independent units that
benefit from isolated context, parallelism, or specialization.

Before delegation, the orchestrator must define for each worker:

- task boundary,
- allowed files or evidence sources,
- non-goals,
- output contract,
- required checks or manual evidence,
- conflict and escalation rule,
- whether the result is advisory, evidence-ready, or blocked.

Worker results are candidates, not final completion. The orchestrator must
synthesize conflicts, check that results fit the active SPEC and source-of-truth
order, and produce one owner-readable evidence summary.

Do not use workers for tightly coupled edits where parallel work will create
merge risk, or for small packets where coordination cost exceeds execution
cost.

## Loop Engineering

Loop Engineering means deciding what starts the next run and what stops it.

| Loop type | Starts when | Stops when | SDAD use |
|---|---|---|---|
| Turn-based | Owner sends a task | Agent returns evidence-ready, blocked, or asks for owner input | Default SDAD work packet |
| Goal-based | Previous attempt finishes but completion condition is not met | Evidence condition passes, budget expires, or blocker appears | Test repair, docs consistency, migration checklist |
| Time-based | Schedule or interval fires | Owner cancels, work naturally ends, or stop rule triggers | PR/CI polling, recurring docs drift checks, dependency watch |
| Event-based | External event arrives | Packet evidence is ready, blocked, rejected, or routed to owner | Issue triage, release event, alert, user evidence import |

Every non-trivial loop must declare:

- trigger,
- goal or done condition,
- maximum turns, runtime, spend, or attempts,
- evidence to collect,
- stop rules,
- owner gate,
- where the loop writes state,
- what must never happen without owner approval.

Time-based and event-based loops should usually live in enforced or automated
surfaces such as CI, scheduler, hook, routine, or workflow. Do not hide them as
chat habits.

## Routing Gate

Before adding Advisor, Worker, or Loop structure, answer:

| Field | Required Answer |
|---|---|
| Packet purpose | What owner-visible outcome this route protects |
| Default executor | The cheapest/simplest agent that can do ordinary work |
| Escalation trigger | When an advisor, stronger model, reviewer, or owner must be consulted |
| Worker boundary | What can be split without merge, context, or ownership conflicts |
| Loop trigger | Turn, goal, schedule, or event |
| Budget | Token/API spend, wall-clock time, attempts, workers, or owner review time |
| Evidence contract | What result makes the packet evidence-ready |
| Stop rule | When the loop stops even if the goal is not met |
| Owner gate | Which decision still requires owner acceptance |
| State surface | Where outputs, findings, memory, and handoff state are recorded |

If these fields are unknown, start with the Lean Execution Contract and a normal
work packet. Do not add orchestration to compensate for unclear scope.

## Evidence Boundary

Cost-aware routing can improve efficiency and review quality. It does not lower
the evidence bar.

- Advisor approval is review evidence, not owner acceptance.
- Worker completion is candidate evidence, not integrated completion.
- A goal loop passing its evaluator is evidence-ready, not final done.
- A scheduled or event-based loop must not make product, release, security,
  money, data, destructive-action, or rollback claims without the matching SDAD
  gate.
- Benchmark ratios from external sources are reference material, not project
  evidence. Evaluate routing on the project's own workload when the cost or
  quality claim matters.

## Stop Rules

Stop or downgrade the route when:

- coordination cost exceeds the saved execution cost,
- advisor calls become routine instead of exceptional,
- workers need too much shared context to remain independent,
- loop attempts repeat without new evidence,
- evidence quality drops because the evaluator is too weak or too close to the
  generator,
- active docs become a transcript of agent chatter,
- the route changes owner-controlled risk without an owner checkpoint.

When stopped, record the route used, budget spent, evidence produced, unresolved
risks, and the next owner decision. Do not convert "the loop kept running" into
"the work is done."
