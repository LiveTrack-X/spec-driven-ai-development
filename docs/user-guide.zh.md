# 用户指南和 FAQ

[English](user-guide.md) | [한국어](user-guide.ko.md) | [中文](user-guide.zh.md) | [日本語](user-guide.ja.md)

本文是中文导览版 user guide。规范文档以英文
[user-guide.md](user-guide.md)、`docs/`、`templates/` 和 `scripts` 为准。
如果本文与英文文档不一致，请以英文规范文档为准。

SDAD 是一种 AI-assisted development 控制方法。它不会自动保证 AI 输出正确，
但会让 scope、evidence、review、handoff 和 owner acceptance 不容易丢失。

## 快速选择

| 场景 | 使用 | 预期结果 |
|---|---|---|
| 一次性请求 | One-shot prompt | 不创建 SDAD files |
| 小任务，但 done 需要证据 | Mini SDAD | 一个 AI instruction file |
| 多会话、评审、TODO 会持续存在 | Standard SDAD | SPEC、TODO、review、docs control files |
| 存在 release、migration、production、user data、auth、money、security、destructive action、rollback 风险 | Full SDAD，或带明确 gate 的 Standard 以上 | review、evidence、必要时 ADR、owner gate |
| Claude.ai、ChatGPT web 等 chat-only 环境 | planning only | 不声称已安装 adapter |

选择能保护项目的最小 scale。risk 优先于简单的 yes 数量。

## SDAD 提供什么

- 使用当前 SPEC，避免旧笔记覆盖 active work。
- 使用 work packet，避免每个 micro-task 都停下来。
- 使用 review-worthy unit，把 evidence 组织成可评审的单位。
- 区分 AI 的 "done"、evidence-ready 和 owner-accepted。
- 把 SPEC 未说明的实现判断记录到 `docs/implementation-notes.md`。
- 用 `save-state.md` 和 handoff 让下一次会话从 repo state 继续。
- 避免大日志、archives、generated files、private data 进入 AI context。

## 问题排查 FAQ

### Q. AI 太频繁请求批准，或者推进得太远。

A. 同时调整 autonomy level、packet boundary 和 operating intensity。

| 症状 | 尝试 | 含义 |
|---|---|---|
| 每个小步骤都询问 | Level 2 Work Packet Autonomy | Owner 批准 packet 边界，内部 micro-task 由 AI 连续处理。 |
| 只需要完成一个 unit 后停止 | Level 1 Unit Autonomy | 一个 review-worthy unit 就是已批准 packet。 |
| setup 是新的、模糊的或有风险 | Level 0 Ask-first | 在边界清楚前，每个有意义的步骤前都询问。 |
| 低风险 session goal 很清楚 | Level 3 Session Autonomy | 推进到 session goal、time box 或 stop condition。 |
| 涉及 release、migration、destructive action、user data、auth、money、security、rollback、production claim | Level 4 Release-gated Autonomy | AI 可以准备工作，但 risk acceptance 和 release decision 保留 owner gate。 |

### Q. AI 在检查 repository 之前就提问。

A. 要求 clarification checkpoint。

```text
Inspect repository evidence first: code, tests, active docs, SPEC, TODOs, review
findings, and ADRs. Ask only the next blocking question, include your
recommended answer, and explain what changes if I choose differently.
```

### Q. AI 只说 "done"，我看不出改了什么。

A. 不要接受 final completion，先要求 evidence-ready status。

需要检查：

- changed files,
- tests/build/lint/manual check，或无法运行的原因,
- docs checked 或 updated,
- 需要的 implementation notes,
- review findings 是否已处理或追踪,
- limitations、partial/degraded/unverified behavior,
- 仍然需要的 owner decision.

### Q. SDAD 文件太多。

A. 使用更小的 scale 或更低的 intensity。

一次性工作用 One-shot prompt。小任务但需要 evidence 时用 Mini SDAD。只有在会维护
control files 时才使用 Standard/Full。

### Q. 下一次会话总是丢失上下文。

A. 会话结束前更新 `save-state.md` 或创建 handoff。

关闭长会话或交给新会话前，创建
`docs/sdad/handoffs/YYYY-MM-DD-topic.md`。不要复制长内容，改为链接 SPEC、TODO、
ADR、review findings、implementation notes 和 evidence path。

### Q. 需要处理 SPEC 没有说明的实现判断。

A. 把判断记录在可见位置。

普通实现判断记录到 `docs/implementation-notes.md`，包括 assumption、compromise、
rejected alternative、tradeoff、follow-up 和 verification impact。只有难以回退、
未来维护者会感到意外、且代表 real tradeoff 的决定才使用 ADR。

### Q. review 发现了 bug。

A. evidence-ready 是 reviewable，不是 owner-accepted。

如果适合当前 packet，就在当前 packet 修复。否则放入 `review-findings.md` 或
`docs/TODO-Open-Items.md`，然后定义下一个 packet。

### Q. chat-only tool 声称已安装 SDAD。

A. 如果不能编辑 project filesystem，就没有真正安装。

Claude.ai、ChatGPT web 可以用于 planning，但不能声称已保存 adapter file。实际安装应在
Codex、Claude Code、Cursor、Copilot Chat 等能编辑 project folder 的 AI coding tool 中完成。

### Q. 任务涉及 release、data、auth、money、security 或 destructive work。

A. 不要只靠提高 autonomy 解决。

使用 Standard 或 Full SDAD，并设置明确 gate。risk acceptance、rollback posture、
production claim、migration、destructive action、real user data handling 仍需 owner
approval。

## 接下来阅读

- [getting-started.md](getting-started.md): setup path 和最初 10 分钟
- [no-clone-quick-install.md](no-clone-quick-install.md): 不 clone 仓库也能开始
- [mini-sdad.md](mini-sdad.md): 小项目用 one-file SDAD
- [autonomy-levels.md](autonomy-levels.md): autonomy level 和 work packet
- [implementation-notes.md](implementation-notes.md): 实现判断记录规则
- [session-handoff.md](session-handoff.md): 长会话 handoff
