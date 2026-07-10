# Context And Data Playbook

Status: On demand
Trigger: large, stale, generated, historical, private, or secret-bearing input

## Progressive Read

Start with `sdad-state.yaml`, `docs/INDEX.md`, current source/tests, and the
smallest routed section that can decide the packet. A route is permission to
inspect the relevant material, not permission to dump every linked file into
context.

Before opening a routed file or broad result set, check size, freshness,
generation source, sensitivity, and relevance. Prefer:

- file metadata and directory shape,
- headings and current-status sections,
- targeted exact or semantic matches,
- bounded command output and explicit excludes,
- links to existing evidence instead of copied logs.

Default soft triggers:

- above 50 KB or 500 lines: use a bounded read;
- above 200 KB or 2,000 lines: run a context-stability check;
- above 1 MB: do not read in full during startup unless the owner requests
  historical reconstruction.

## Sensitive Data Boundary

Sensitive data is an authorization boundary, not a size threshold. Use
metadata-only inspection by default. Reading content requires both a real task
need and permission from owner policy plus tool policy.

Do not place credentials, private keys, tokens, cookies, `.env` contents, raw
customer records, or private corpora in prompts, logs, TODOs, findings,
handoffs, generated artifacts, or external services. Prefer redacted samples,
schemas, counts, filenames, and hashes. Stop before reading when authorization
is unclear.

## Context Recovery

If a session becomes unstable, first suspect oversized state files, broad
searches, generated output, copied logs, private data, or old archives. Save a
small current handoff, restart with the active state and SPEC, then reload only
the routed slices. Do not change runtime code merely because the chat context
became noisy.
