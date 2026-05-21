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
- 用 context layer 区分现在必须读取、按需读取、以及只应通过 bounded evidence 引用的内容。
- 用 before/after change guard，让 autonomy 留下可审计痕迹。

## SDAD 如何组织 context

| layer | 示例 | 使用方式 |
|---|---|---|
| always-loaded instructions | `AGENTS.md`, `CLAUDE.md`, Cursor/Copilot rules | 每次会话都可读取，必须短且当前有效。 |
| active control files | 当前 SPEC、TODO、review findings、implementation notes、save-state | 读取当前 packet 需要的相关部分。 |
| on-demand references | pattern catalog、anti-patterns、field notes、localized guides | 只有当前问题需要时再打开。 |
| archive and evidence | 旧 handoff、logs、generated reports、historical notes | 用 path 或 bounded read 引用，不默认整段贴进 chat。 |

如果 AI 迷失方向，先让它说明 active packet、source of truth 和缺少的 evidence，
不要第一步就加载更多历史。

## 自然语言请求

用户不需要记住 SDAD 术语、adapter 名称或 skill 名称。用普通语言说明想做的
事即可。AI 应该推断 intent，选择最小且安全的 SDAD route，并简短说明它如何
理解请求。

| 你这样说 | AI 应这样理解 |
|---|---|
| "帮我整体检查", "看看有没有问题", "找 bug" | review 或 audit intent |
| "实现这个", "修复它", "按 SPEC 做" | SPEC implementation intent |
| "release", "publish", "tag" | 带 Level 4 owner gate 的 release intent |
| "文档太难懂", "写 guide", "加 FAQ" | documentation intent |
| "之后继续", "handoff", "下个 session 会丢上下文" | handoff 或 save-state intent |
| "这个 repo 有什么可以借鉴?" | reference-intake intent |
| "它太常请求批准", "它跑得太快" | autonomy tuning intent |

如果 intent 明确，AI 应继续执行并简短说明自己的解释。如果多个 intent 冲突并
会改变 scope 或 risk，AI 只问一个 blocking clarification question，并给出
推荐默认答案。

## 问题排查 FAQ

### Q. 我不知道正确的 SDAD 命令或 skill 名称。

A. 用自然语言请求，让 AI route intent。

示例：

- "检查这个 repo 里可能有问题的地方。"
- "按当前 SPEC 实现，并记录 SPEC 没写明的判断。"
- "它请求批准太频繁了。调整这个 packet 的 autonomy level。"
- "准备 release，但 release 和 rollback decision 保留 owner gate。"
- "把 README 改得更适合第一次使用的人。"
- "创建 handoff，让下个 session 能继续。"

AI 应先简短说明 interpreted intent、SDAD scale/intensity、autonomy level、
需要的 evidence，以及 owner gate。如果这种解释会改变 risk 或 scope，继续前
只问一个 clarification question。

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

### Q. 不确定任务大小。

A. 按 continuity 和 risk 分类，不要只看预计代码行数。

| 信号 | 使用 |
|---|---|
| 一次性答案、文案修改、无需未来上下文的小变更 | One-shot prompt |
| 小变更，但 done 需要证据 | Mini SDAD 或 Level 1 Unit Autonomy |
| 有关联的 docs、prompt、template、code 更新 | Standard SDAD + Level 2 Work Packet Autonomy |
| 多文件 behavior change、重复 bug、review findings、context loss | Standard SDAD / Medium 或 High |
| release、migration、destructive action、production claim、real user data、auth、money、security、rollback | Full SDAD 或带 Level 4 gate 的 Standard 以上 |

### Q. 修改文件前后应该检查什么？

A. 使用轻量 before/after change guard。

修改前确认 active SPEC、work packet、autonomy level、allowed scope、non-goals、
owner gate 和 stop condition。

修改后报告 changed files、checks run、docs checked/updated、是否需要
implementation notes、limitations、unverified behavior 和 owner decision。

### Q. 没有 formal test 时，什么 evidence 足够？

A. 使用当前可获得的最强 practical evidence，并标明限制。

例如 build/lint/typecheck output、targeted script、smoke test steps、curl/API
response、application logs、screenshot、manual reproduction note、docs diff、
unverified behavior 列表。

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
- [context-stability.md](context-stability.md): context layer 和 bounded read
- [autonomy-levels.md](autonomy-levels.md): autonomy level 和 work packet
- [implementation-notes.md](implementation-notes.md): 实现判断记录规则
- [session-handoff.md](session-handoff.md): 长会话 handoff
