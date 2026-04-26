# CMP Development Method Field Note

Status: Active reference
Scope: Reusable operating patterns extracted from the Connect Memory Project

This note extracts the development method, not product internals. CMP is useful
as a field example because it shows how a large AI-assisted project can keep
many SPEC revisions, active docs, reviews, hardening tracks, and owner decisions
from collapsing into chat memory.

## What CMP Teaches

### 1. Start From A Documentation Router

CMP requires every agent to start from `docs/INDEX.md` before touching code,
SPECs, prompts, or documentation. The index is not a passive table of contents.
It is the repository router:

- which docs are active,
- which docs are historical,
- which docs are only product notes,
- which SPEC files are current,
- which backlog and review files must be read.

Reusable rule: every serious AI-driven project needs one current navigation
document that answers "what should this agent read now?"

### 2. Keep A Mandatory Start Loop

CMP's agent entry sequence is:

1. read the documentation index,
2. read repository operating rules,
3. read active docs routed from the index,
4. read open TODOs and review findings for implementation work,
5. inspect source code and tests before implementing from a plan.

Reusable rule: never let a fresh AI session begin from an old handoff, archived
plan, or impressive SPEC without first checking the current route.

### 3. Define Source Of Truth Order

CMP explicitly ranks evidence:

1. source code, migrations, and tests,
2. active runtime docs,
3. canonical integrated SPEC,
4. active or planned SPEC files,
5. current handoff files,
6. product notes and external references,
7. historical or archived records.

Reusable rule: SPECs can define intent, but implementation status must come from
code, tests, migrations, and repeatable commands.

If a SPEC spans past-to-present history, current active sections override older
sections. Older sections remain useful rationale but should not drive new
implementation unless reaffirmed in the active route.

### 4. Split Current Work From Review Findings

CMP uses different files for different kinds of unfinished work:

- `docs/TODO-Open-Items.md` tracks open implementation work.
- `review-findings.md` tracks active defects, hardening findings, and review
  backlog.
- archived docs preserve rationale but do not drive current implementation.

Reusable rule: do not bury bugs in prose handoffs. Give defects a durable
review ledger and implementation gaps a durable TODO ledger.

### 5. Require Documentation Consistency Checks

CMP uses minimum documentation update sets. A code change that touches security,
configuration, retrieval, worker lifecycle, prompts, roadmap status, or open gap
status implies a specific set of docs to check or update before handoff.

Reusable rule: every implementation handoff must say either which docs changed
or which docs were checked and why no content change was needed.

### 6. Separate Core Completion From Production Readiness

CMP distinguishes "feature-rich v1 candidate" from "production-ready." Production
readiness is its own hardening track covering security, migration proof, backup
safety, observability, scale evidence, runtime settings policy, and rollback
posture.

Reusable rule: completion percentages must name the scope. A project can be
mostly implemented for local/core use while still not production-ready.

### 7. Promote External Ideas Deliberately

CMP keeps external references and adoption notes under product-note routes until
they are promoted into active SPECs. This prevents interesting research from
silently becoming required work.

Reusable rule: future ideas need a promotion step before builders treat them as
implementation requirements.

### 8. Use Evidence-Based Status, Not AI Confidence

CMP status is strongest when tied to focused test commands, migration checks,
audit commands, docs checked, and known remaining gaps. AI confidence is not a
valid completion artifact by itself.

Reusable rule: ask every builder and reviewer to include commands run, results,
files changed, docs checked, and remaining risks.

## Reusable CMP Rule Pack

Add these rules to projects with heavy docs, many SPEC revisions, or multiple AI
sessions:

- A single `docs/INDEX.md` must route all active docs and archives.
- `docs/Repository-Operating-Rules.md` must collect repeated rules that would
  otherwise stay in chat.
- `AGENTS.md` must require the first-read chain.
- `docs/TODO-Open-Items.md` and `review-findings.md` must stay active and
  separate.
- Historical docs must be preserved but clearly excluded from the execution path.
- Code changes must include a documentation consistency check.
- Production readiness must be a named gate, not an assumption.

## When To Use This Pattern

Use the CMP-style controls when:

- the project has long-lived SPECs,
- multiple AI sessions or models will contribute,
- the owner needs progress visibility without writing code,
- docs are likely to multiply,
- production-readiness claims are risky,
- external research can easily overwhelm active implementation.
