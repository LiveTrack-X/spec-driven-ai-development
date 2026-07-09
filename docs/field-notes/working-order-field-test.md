# Working Order Field Test

Status: Active reference
Scope: Multi-agent disposable-project test of the SDAD Working Order

This note records a field test of the SDAD Working Order:

```text
Route current state -> Scale/compress -> PLAN -> Active SPEC -> optional ADR -> TODO/work packet -> JIT clarification -> Build/review/evidence -> Owner checkpoint/maintenance
```

The test used four independent disposable projects under
`C:\Users\livet\Desktop\SDAD-Flow-Agent-Lab`. The goal was not to prove SDAD in
general, but to look for places where a working agent may misunderstand the
routine, overclaim evidence, skip documentation records, or let active files
grow into journals.

## Test Matrix

| Lane | Disposable project | Cycles | Evidence checked | Result |
|---|---|---:|---|---|
| Mini CLI | `mini-cli` | 2 | `python mini_cli.py review`; `python -m py_compile mini_cli.py` | Passed after state-file bug fix |
| Reference parity | `web-ref-parity` | 2 | `node parity-check.js cycle-2`; `node --check app.js`; `node --check parity-check.js` | Passed after parity bug fix |
| Claim/evidence package | `claim-evidence-package/cycle1-disposable` | 2 | `python -m pytest -q`; claim review CLI | Tests passed; production claim remained blocked |
| Handoff/bloat loop | `handoff-bloat-loop/run-20260709-140345` | 3 | `run_summary.json`; `handoff/latest.json`; timestamped log and split evidence files | Completed with bloat split evidence |

## Findings

### 1. The Working Order Is Usable, But Cycle Results Need A Small Record

Agents could follow the order when it was explicit. The recurring gap was not
the order itself; it was the shape of the result after a failed or corrected
cycle.

Reusable rule: for every failed, fixed, or release-readiness cycle, record:

- problem,
- cause,
- action taken,
- evidence command or artifact,
- residual concern.

This keeps "we fixed it" from replacing proof of what changed and why.

### 2. Reference Parity Needs Artifact-Appropriate Evidence

The web parity lane caught a real behavior mismatch: `clearCompleted` removed
only the first completed item instead of all completed items. The parity gate
worked because it compared source behavior, implemented behavior, and evidence.

The lane also showed a false-check risk: `node --check styles.css` is not a
valid CSS or browser-render check. It is only a tool mismatch.

Reusable rule: choose evidence by artifact type. JavaScript syntax checks do not
prove CSS validity, HTML rendering, browser behavior, persisted state, or live
runtime behavior. For UI claims, use browser render, DOM checks, visual review,
or live runtime evidence when the claim requires it.

### 3. Passing Tests Can Coexist With A Blocked Claim

The claim/evidence package passed local tests, but its production claim remained
blocked because no production evidence existed. The claim review returned a
non-zero result for the blocked claim, which was correct behavior.

Reusable rule: a local test pass may support local behavior claims while a
release, production, hardware, compatibility, or rollback claim remains blocked.
Do not convert a green test suite into a stronger evidence tier.

### 4. Bloat Controls Work, But Counters Need Meaning

The handoff/bloat lane generated timestamped logs and split a long record into
`bug_notes_long_compressed_Start-...md`. That matched the intended archive
pattern.

The lane also showed that status counters can be ambiguous. A `cycle_log_count`
or similar field should say whether it was captured before or after the owner
checkpoint.

Reusable rule: when a handoff reports counts, state the boundary:
`checkpoint_included`, `pre_checkpoint`, or `post_checkpoint`.

### 5. Shell And Encoding Friction Can Masquerade As SDAD Failure

The Mini CLI and handoff lanes both hit practical Windows issues:

- bash heredoc examples do not work in PowerShell,
- console encoding can corrupt non-ASCII evidence text,
- folder names with spaces increase follow-up script risk.

Reusable rule: evidence commands should match the active shell. For Windows
handoffs, prefer PowerShell-safe commands, machine-safe folder slugs, and UTF-8
notes when non-ASCII text is evidence.

## Recommended SDAD Adjustments

Keep the core framework small. Do not add a mandatory harness for every project.
Instead, preserve these lightweight checks:

- Add a cycle result record to evidence-ready or handoff summaries when a cycle
  failed, was fixed, or changed release/readiness status.
- In reference parity work, require artifact-appropriate evidence and at least
  one edge-case trace or a short rationale for why no extra trace is needed.
- Treat claim-review failures as valid evidence when they intentionally block
  unsupported claims.
- Label handoff counters by boundary when they can be read before or after an
  owner checkpoint.
- Keep disposable field-test projects outside the SDAD repo and record only the
  reusable finding in field notes.

## Evidence Boundary

This field note is not owner acceptance of the disposable projects. It is
evidence that the SDAD Working Order can be followed across different task
shapes and that the listed friction points are worth preserving as operating
guidance.
