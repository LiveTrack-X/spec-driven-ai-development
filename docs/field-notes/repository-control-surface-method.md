# Repository Control Surface Method

Status: Active reference
Scope: Tool-neutral repository structure for AI coding control surfaces

This note adapts modern AI-coding repository-setup practices into SDAD. The
useful idea is not a specific folder tree for one tool. The useful idea is that
AI behavior is shaped by several control surfaces, and each surface should carry
the kind of rule it can actually support.

Use this pattern when a project keeps asking the same prompts, losing the same
context, skipping the same checks, or relying on one large instruction file to
carry rules that should be routed, automated, or enforced.

## SDAD Translation

Repository structure is part of the SDAD control layer. It should answer:

- what the AI should always know,
- what it should load only for a specific path, domain, or intent,
- what repeated procedures should become reusable playbooks,
- what exploration should happen in an isolated context,
- what non-negotiable behavior must be enforced by tools, not reminders,
- what project memory is reviewed, versioned, and safe to reuse.

Do not turn this into maximum bureaucracy. The goal is smaller startup context,
stronger guarantees, and easier owner review.

## Control Surface Ladder

| Surface | SDAD role | Good examples | Not good for |
|---|---|---|---|
| Always-loaded guidance | First-read rules every AI session should see | adapter file such as `AGENTS.md`, `CLAUDE.md`, Cursor or Copilot instructions | Long tutorials, historical logs, raw evidence |
| Routed guidance | Rules loaded only for a domain, path, risk area, or intent | domain rules, API rules, release rules, security review prompts | Global rules every session must remember |
| On-demand procedure | Repeatable steps called only when needed | skills, checklists, review playbooks, release playbooks | Non-negotiable safety guarantees |
| Isolated exploration | Research that should not flood the main working context | bounded subagent, separate review pass, candidate branch, workflow run | Owner acceptance or final completion |
| Enforced guarantee | Behavior that must happen or must be blocked | CI, tests, validators, hooks, permissions, deny rules, protected release gates | Style guidance or nuanced owner tradeoffs |
| Reviewed memory | Durable lessons the next session may trust | implementation notes, ADRs, operating rules, handoffs, trace links | Hidden chat memory, unreviewed auto-memory, secrets |

Each surface should stay in its lane. A Markdown rule can guide an AI, but it
should not be the only protection for secrets, destructive commands, production
deployments, migrations, release assets, or money/data/security boundaries.

## Guidance vs Enforcement

Use guidance when the rule requires judgment:

- naming style,
- domain vocabulary,
- review posture,
- source-of-truth order,
- owner checkpoint criteria,
- when to create an ADR instead of an implementation note.

Use enforcement when the behavior must be deterministic:

- secret scanning,
- required tests, lint, or validators,
- blocked destructive commands,
- migration safety checks,
- release artifact verification,
- production deploy gates,
- generated artifact ignore rules.

If the project would be unsafe when the AI follows a rule only most of the time,
the rule belongs in an enforced surface or a release/risk gate. Keep the
Markdown version as a readable explanation, not as the only control.

## Routing Rule

When repeated work appears, route it by type:

| Repeated work | Route to |
|---|---|
| Research, comparison, or broad inspection | Isolated exploration with a bounded summary |
| Procedure, checklist, or multi-step habit | On-demand procedure |
| Must-run check or must-not-do action | Enforced guarantee |
| Expensive or high-risk judgment inside an otherwise executable packet | Cost-aware advisor checkpoint |
| Independent subtasks with separate evidence needs | Orchestrator-worker packet |
| Recurring, scheduled, or event-triggered work | Bounded loop with trigger, budget, and stop rule |
| Durable rationale or owner tradeoff | ADR |
| Spec-unstated implementation choice | Implementation notes |
| Repeated failure or confusion | Operating rule, test, validator, template, or review gate |

This keeps the main context readable while still turning repeated pain into
reusable structure.

For advisor, worker, and loop routing, see
[cost-aware-agent-routing-method.md](cost-aware-agent-routing-method.md).

## Minimal Layout

Do not require every project to create every folder. Start with the smallest
layout that protects the current work:

```text
project/
  AGENTS.md or CLAUDE.md or tool-specific adapter
  sdad-state.yaml
  docs/
    INDEX.md
    Repository-Operating-Rules.md
    sdad/playbooks/
    TODO-Open-Items.md
    implementation-notes.md
    sdad/handoffs/
  SPEC/
    SPEC-COMPLETE.md
    adr/
  scripts/
    validators or release checks
  review-findings.md
  save-state.md
```

Add routed rules, skills, hooks, CI jobs, or agent workflows only when repeated
pain proves the need. For One-shot or Mini SDAD, keep the same principle but
collapse the surfaces into a small instruction file and a short evidence-ready
summary.

## Bloat Controls

- Keep always-loaded instructions short enough to read at every session start.
- Move long explanations to on-demand docs or field notes.
- Move current work state to TODO, review findings, SPEC, and save-state, not
  to tool-specific global instructions.
- Move raw logs and large traces to archive/evidence paths with IDs.
- Promote repeated safety checks to validators or CI instead of more prose.
- Promote repeated owner tradeoffs to ADRs only when they are hard to reverse.
- Remove or archive rules that no longer change behavior.

## Control Surface Checkup

Use a control surface checkup when context bloat, duplicated local and checked-in
instructions, stale plugins or MCP servers, unused skills, slow hooks, repeated
permission denials, or tool-version drift starts to slow the project or confuse
agent routing.

The checkup is a report-first routine. It may recommend:

- unused skill, MCP, plugin, hook, or rule cleanup,
- deduplicating local tool instructions against checked-in adapter files,
- splitting one large root instruction file into routed guidance or on-demand
  procedures,
- disabling or replacing slow hooks,
- updating an AI coding tool,
- changing auto mode, permission defaults, or read-only command approvals,
- moving repeated procedures into skills/playbooks and guarantees into
  validators, CI, hooks, permissions, or deny rules.

Report-only checkup output can be evidence-ready when it lists inspected
surfaces, proposed changes, expected context savings or routing benefit, and
risks. Applying the changes is a separate owner checkpoint whenever it changes
installed tools, permissions, hooks, auto mode, source-of-truth routing,
enforced guarantees, or default access to local/private data.

Do not let a cleanup routine silently remove rare but critical tools, disable a
safety hook, enable broader autonomy, or pre-approve commands just because they
are usually read-only. Treat those as risk-gated control-surface changes.

## Evidence Boundary

Repository structure can make AI work more reliable. It is not completion
evidence by itself.

Evidence-ready still requires changed files, checks, relevant docs reviewed,
known limits, and risk status for the active packet. Owner-accepted still
requires the owner checkpoint or delegated acceptance policy. A new control
surface is only adopted when the owner can see what behavior changed, what is
enforced, what remains guidance, and how to roll it back.

## Adoption Checklist

Before adopting this pattern, answer:

- Which rules must be seen every session?
- Which rules are path, domain, risk, or intent specific?
- Which repeated procedures should become a playbook or skill?
- Which broad research tasks should be isolated from the main context?
- Which guarantees must be enforced by tooling?
- Where does reviewed project memory live?
- Which generated, private, local, log, dependency, or evidence surfaces must
  stay out of default AI context?
- What owner checkpoint accepts the new structure?

If these answers create more active docs than the owner can review, reduce the
scope. SDAD control surfaces should make the project easier to supervise, not
harder to enter.
