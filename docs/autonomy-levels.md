# Execution Scope And SDAD 3.1 Migration

Current SDAD Protocol work separates three controls:

| Control | Owns | Does not own |
|---|---|---|
| Scale | Persistent control surface | Work authorization |
| Execution scope | Current `unit` or `packet` boundary | Risk acceptance |
| Owner gate | Permission for a protected action | Implementation quality |

For state v2, `execution_scope` is exactly:

```text
unit | packet
```

`ask_first` is an approval condition, not a scope. A session is a tool or time
boundary, not a work boundary. Multi-packet work requires an explicitly
approved packet plan or list.

## Current Defaults

| Scale | Default execution boundary | Owner control |
|---|---|---|
| One-shot | Current request only | Ask for protected actions |
| Mini | `unit` | Ask for protected actions |
| Standard | `packet` | Named gates as applicable |
| Full | `packet` | Named gates for applicable risks |

Evidence-ready means the validation contract has bounded evidence. It is not
owner acceptance.

## Migrating From SDAD 3.1

Numeric autonomy and operating intensity are state-v1 vocabulary. Preserve
them when reading or reporting a v1 project, but do not write them into state
v2.

| Legacy v1 term | Current interpretation |
|---|---|
| Level 0 Ask-first | No execution authorization yet |
| Level 1 Unit Autonomy | `execution_scope: unit` |
| Level 2 Work Packet Autonomy | `execution_scope: packet` |
| Level 3 Session Autonomy | Explicitly approved multi-packet plan; never a scope enum |
| Level 4 Release-gated Autonomy | Named owner gates, independent of execution scope |

High, Medium, and Low remain historical v1 operating-intensity inputs only.
Migration starts with a read-only preview and preserves the v1 contract until
the owner accepts the v2 write.
