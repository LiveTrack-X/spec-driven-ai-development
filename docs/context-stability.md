# Context Stability & Bounded Reads

Status: Active reference
Scope: Tool-agnostic rules for keeping AI coding sessions readable and stable

SDAD treats chat context as a scarce operating resource.

The goal is not to hide project history. The goal is to keep fresh AI sessions
able to start from current, bounded, auditable context instead of loading large
logs, generated artifacts, old journals, or private data into the chat.

## Operating Model

- Active control files are routing summaries, not permanent logs.
- Archives preserve history, but they are not the default startup path.
- Generated files, logs, local databases, private corpora, and tool caches are
  not default AI reading material.
- Fresh sessions should resume from current summaries, active specs, handoffs,
  and targeted repository inspection.
- If an AI chat becomes unstable, first suspect context growth from large files
  or broad searches before changing runtime code.

## Bounded Read Rule

Context Stability applies before any mandatory start-loop read.

Before opening any routed document, archive, generated artifact, log, or search
result, check whether the input is large, stale, private, generated, or outside
the active scope.

Use bounded reads:

- check file size before reading large control files,
- read headings, current sections, first/last sections, or matching sections,
- prefer targeted searches with output limits,
- use explicit include and exclude paths,
- avoid broad recursive searches over logs, caches, generated output, private
  data, local databases, dependency directories, or session transcripts,
- quote or paste only the specific lines needed for the current decision.

Do not treat a mandatory start loop as permission to dump every routed file into
the AI chat context.

## Soft Size Triggers

These are default review triggers, not hard failures:

- `>50 KB` or `>500 lines`: use bounded reads by default.
- `>200 KB`, `>2,000 lines`, or hard to audit: run a context-stability check
  before feature work continues.
- `>1 MB`: do not read in full during startup unless the owner explicitly asks
  for historical reconstruction.

If the project has stricter local limits, record them in
`docs/Repository-Operating-Rules.md`.

## Live-State Size Budget

Files such as `save-state.md`, `next-task.md`, `review-findings.md`, and
`docs/TODO-Open-Items.md` should stay short enough to read as active operating
state. Treat `docs/implementation-notes.md` the same way when a project uses it:
it is current decision context, not a permanent thought journal.

If a live-state file becomes long, repetitive, or hard to audit:

1. Preserve the old material in an archive or history location.
2. Keep the active file focused on current objective, open items, constraints,
   validation state, next one to three steps, and archive links.
3. Update `docs/INDEX.md` or the project routing document so fresh sessions know
   where active summaries and historical records live.
4. Read archive/history files only through targeted headings or keyword searches
   unless the owner explicitly requests historical reconstruction.

Do not delete history just to reduce context. Move it out of the default startup
path.

## Tool Input Hygiene

Context stability also applies to tools that package or index repository
content.

If the project uses graphing, repo-packing, search, embedding, indexing, or
context-building tools, keep their ignore files aligned with the bounded-read
rule. Common examples include:

```text
.gitignore
.graphifyignore
.repomixignore
.cursorignore
.aiignore
```

Ignore files should exclude local session state, generated artifacts, logs,
private data, local databases, dependency directories, build output, and tool
caches unless the owner explicitly chooses them for the current packet.

## Suggested Storage

Use project-appropriate archive paths. Common patterns:

```text
docs/state/save-state-archive/YYYY-MM-DD-topic.md
docs/state/next-task-history/YYYY-MM-DD-topic.md
docs/review/archive/YYYY-MM-DD-topic.md
docs/archive/todo-history/YYYY-MM-DD-topic.md
docs/archive/YYYY-MM-DD-topic.md
```

## Handoff Requirements

When context stability work happens, the handoff should include:

- which active files were slimmed or rerouted,
- where historical material was preserved,
- which large files or directories should not be read in full,
- which bounded-read commands or patterns were used,
- whether validation passed after moving history,
- the next active file a fresh session should read first.

## What This Is Not

This rule does not add cleanup automation, archive automation, log rotation,
worktree pruning, database mutation, or automatic maintenance behavior.

It is a read discipline and documentation-shaping rule: keep the active context
small, preserve history explicitly, and make fresh sessions reliable.
