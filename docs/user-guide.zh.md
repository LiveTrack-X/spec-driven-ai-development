# 用户指南和 FAQ

[English](user-guide.md) | [한국어](user-guide.ko.md) | [中文](user-guide.zh.md) | [日本語](user-guide.ja.md)

本文是中文导览版。英文 [user-guide.md](user-guide.md)、`docs/`、`templates/`、
`scripts/` 是英文规范文档。如有差异，以英文规范为准。

SDAD Protocol（SPEC-Directed AI Development）是一套用于 AI 辅助开发的
repository-local 运行协议。它不规定实现方法或 AI 工具，而是持续保持当前 scope、
validation、evidence、unresolved state 与 Owner authority 的一致性。它不保证 AI
一定正确，也不取代 tests、CI、permissions 或 review。

## 先区分三个轴

> Scale 决定维护哪些 control files，`execution_scope` 决定 AI 现在可以推进到哪里，
> owner gate 决定哪些操作必须停下等待 Owner。

| 轴 | 负责什么 | 不负责什么 |
|---|---|---|
| Scale | 需要维护的 control surface | 工作授权范围 |
| `execution_scope` | `unit` 或 `packet` 的执行边界 | 风险接受 |
| owner gate | 受保护操作的权限 | 实现质量 |
| validation contract | 检查和证明范围 | owner acceptance |
| handoff | 会话间的恢复指针 | 当前 source of truth |

## 快速选择

| 场景 | Scale | 默认值 |
|---|---|---|
| 只处理当前请求，不需要持久文件 | One-shot | 当前请求，不创建 SDAD files |
| 小功能或 bug fix | Mini | `execution_scope: unit` |
| 需要多会话、review、TODO、持久 state | Standard | `execution_scope: packet` |
| 存在 release、migration、security、data、production 风险 | Full | `execution_scope: packet` + 必要 owner gates |

平时用户只需说明目标。AI 应根据 repository 和请求先做推断；只有无法判断的项目会实质改变
Scale 或 owner gate 时，才提出一个带推荐答案的 blocking 问题。

推荐的解释报告：

```text
Scale: Standard
Execution scope: packet
Reason: multi-session state and review findings already exist.
Owner gates: release only
Unresolved question: none
```

## 自然语言请求

无需记住正确的 SDAD 命令或 skill 名称。

| 这样说 | AI 应解释为 |
|---|---|
| “整体检查并找出问题” | review/audit intent |
| “按当前 SPEC 实现” | implementation intent |
| “在 release 前停下” | 带 release owner gate 的 packet |
| “让下一会话可以继续” | handoff intent |
| “找出这个 repo 中值得采用的内容” | reference-intake intent |
| “它请求批准太频繁” | `execution_scope` 与 owner-gate 授权/到期调整 intent |
| “commit and wait” | 在 commit 停止；不表示有 push/release/deploy 权限 |

“carefully”“fully”“quickly”等修饰词只改变评审深度或压缩程度，不会扩大 scope。
即使达到 `evidence-ready`，在 Owner 验收前也不是最终完成。
当前适用的 Owner 指令优先于旧方向。方向改变时，应停止受影响的工作，返回 Plan -> Route，
并重新对齐 SPEC/state。明确的祈使命令只授权其点名的 action 与 boundary；问题、假设、引用、
否定句或 review/reference-only 请求，不授权其中提到的 action。

## 一个工作循环

1. Plan — 定义 goal、scope、acceptance、evidence 与 gate。
2. Route — 沿 adapter、state、INDEX 只选择必要文档。
3. Implement — 以小而可评审的 unit 完成修改。
4. Verify — 运行 validation，收集结果与限制。
5. Report — 提交 evidence-ready report。

Owner Gate 只在存在受保护操作时使用，Handoff 只在需要跨会话连续性时使用。它们是条件式
checkpoint，不应成为每个 packet 都必须增加的步骤。

## Context 读取顺序

Standard/Full 启动时使用以下顺序：

```text
tool adapter -> sdad-state.yaml -> docs/INDEX.md -> current source/tests -> selected routed docs
```

`routed_docs` 是当前 packet 可以选择的文档集合，不是 startup 时全部读取的命令。只打开当前
intent 所需的文档，并在 final report 中记录实际读取的路径。archive、大型 log、generated
report、private data 不应默认进入 context。
即使旧 `routed_docs` 未列出当前 Owner 直接指定的 input，也可在请求范围内检查；若采用，
必须在 stateful implementation 前更新 authority 与 route。

大型 Copy-Paste/bootstrap prompt 只在安装或升级时使用一次。安装后不要在每个会话重新阅读或
粘贴，而应遵循 adapter -> state -> INDEX。

工具原生的 session、checkpoint、doctor 功能只是便利功能或 tool diagnostics，不能替代
SDAD 的 `sdad-state.yaml`、`current_handoff` 或 Doctor report。

## State 与 handoff

在 state v2 中，`current_handoff` 是唯一可选的当前连续性指针。如果存在，其文档中的
packet marker 必须与 active packet 一致。不要把长内容复制到 handoff；应链接 SPEC、TODO、
findings、ADR、evidence 的路径，并记录下一步操作。

`save-state.md` 是 v3.1 migration 时读取的 legacy input。迁移到 v2 后，不要继续把它当作
第二份当前 state 更新。仅在需要时创建
`docs/sdad/handoffs/YYYY-MM-DD-HNNNN-topic.md`。`HNNNN` 只在同一日期内递增，
新日期的第一个 handoff 重新从 `H0001` 开始。不同日期可以出现相同 `HNNNN`，因此应使用
完整 path 引用。保留已有的无编号 handoff，只有 `current_handoff` 决定当前 handoff。

## 复用 Owner gate 批准

条件式预先授权可使用以下 exact field 记录：

```text
Decision:
Authorized action:
Packet:
Conditions:
Source/artifact identity:
Expires when:
Evidence required before action:
```

当 `Authorized action`、`Packet`、`Conditions`、`Source/artifact identity`、
`Evidence required before action` 均未变化且尚未达到 `Expires when` 时，不要重复请求同一批准。其中任何一项
发生变化，授权即过期，必须取得新的 Owner 决定。
后续限制、取消或撤销会立即终止受影响的 authorization。若没有替代 packet，则记录为
`deferred`，将 resume trigger 固定为 Owner 明确重新激活，并且不得自动恢复。

## 一个事实只记录在一个位置

| 内容 | 规范位置 |
|---|---|
| 预期 scope、behavior 与 acceptance criteria | state 声明的 `active_spec` |
| 已观察 behavior | 当前 source、tests、runtime 与可复现命令 |
| 小型的非 SPEC 实现判断 | `docs/implementation-notes.md` |
| 难以撤销的结构决定 | ADR |
| 未解决工作 | TODO 或 finding |
| Owner authorization 或 acceptance | 一个权威 owner-decision record |
| 下一会话的恢复信息 | handoff |
| 当前执行 state | `sdad-state.yaml` |

handoff 不复制这些文档的内容，只链接路径和关键结果。
`SPEC-COMPLETE.md` 中的 COMPLETE 表示已集成 baseline，而不是不可变的最终版本。
在 stateful project 中，`active_spec` 是唯一 normative SPEC entrypoint。文件的存在、名称、
日期或 status 本身不会产生 SPEC authority。Owner 指示采用、纳入或实现时，它是当前 change
request；应停止受影响的工作并与 active boundary 对齐。review、compare、explain、
draft/reference-only 请求保持 read-only，仅被发现的 SPEC 也没有自动 authority。同一未完成的
acceptance boundary 可 amend 当前 packet；重大变更或 accepted packet 之后的变更使用新的
packet ID 与 validation。

state 离开 terminal packet 之前，一个 durable decision record 必须同时固定 packet ID、
active SPEC path 与 exact revision、source/artifact identity、evidence 与 claim limits、
unresolved risk 和 final owner decision。

owner-decision record 表示每项 decision 只有一个权威来源，并不要求单一 global file。
修正、限制或撤销 terminal decision 时，不要改写旧 record；应创建带 unique ID 的新
record，填写 `Revises/supersedes`，并移动受影响的 current-claim pointer。
如果 parallel decision 修改同一 predecessor 且 claim scope 重叠，应 hold affected claim；
在 owner reconciliation record 处理所有 competing successor 前，不得用 date 或 ID
选择 current authority。

当 SPEC、source、dependency、environment、artifact、gate 或外部结果变化时，长期
工作必须重新进入 Plan -> Route。只有未完成 objective 与 acceptance 边界都相同时才
保留原 packet。read-only review 或 planning 可以省略 Implement，但报告必须标明 N/A
或 blocked 原因，且不能声称获得了被省略 phase 才能产生的 evidence。

## Evidence 与声明边界

| evidence | 可以说明 | 不能说明 |
|---|---|---|
| Doctor green | 声明的结构彼此一致 | 功能正确、有效、Owner 验收 |
| task benchmark 成功 | 指定 task 成功 | 整体优于旧方法 |
| controlled comparison 成功 | 在比较条件下有所改进 | 自动适用于其他条件 |

AI 只说 done 时，应要求包含 changed files、checks、docs checked、limits、
partial/degraded/unverified behavior、open findings、所需 Owner decision 的
`evidence-ready` report。`owner-accepted` 是另一种状态。

## 问题排查 FAQ

### AI 在检查 repository 之前就提问

先让它检查 code、tests、active docs、SPEC、TODO、findings、ADR。只有之后仍有会改变 Scale 或
gate 的不确定项时，才允许提出一个带推荐答案的问题。

### 批准请求太多，或 AI 推进太远

检查 `execution_scope` 是 `unit | packet` 中哪一个。要连续处理一组 micro-task 时使用
`packet`。连续执行多个 packet 时，Owner 必须明确批准包含 packet list 的 plan。
时间边界 session 不是执行范围值。

### SDAD files 太多

不需要连续性时使用 One-shot，小任务使用 Mini。即使是 Standard/Full，也不要读取全部
`routed_docs`，只选择当前 intent 所需内容。

### 没有 formal test

使用当前最强的 practical evidence 并说明限制，例如 build/lint/typecheck、targeted script、
smoke test、API response、log、screenshot、manual reproduction、docs diff。

### chat-only tool 声称已经安装

如果不能编辑 project filesystem，就没有真正安装。Claude.ai 或 ChatGPT web 只能用于
planning，实际 adapter 安装必须在 coding tool 中完成。

## 接下来阅读

- [getting-started.md](getting-started.md): 安装和首次运行
- [no-clone-quick-install.md](no-clone-quick-install.md): 无 clone 的 one-time bootstrap
- [mini-sdad.md](mini-sdad.md): 小型 project
- [owners-guide.md](owners-guide.md): Owner 操作指南
- [ai-work-loop.md](ai-work-loop.md): 工作循环
- [session-handoff.md](session-handoff.md): handoff contract
- [implementation-notes.md](implementation-notes.md): 实现判断记录

## 使用过 v3.1 术语时

本节仅用于 migration/history。Level 0 Ask-first 可视为尚未批准，Level 1 Unit Autonomy 映射为
`unit`，Level 2 Work Packet Autonomy 映射为 `packet`。Level 3 Session Autonomy 不应把 session
变成 scope，而应写成已批准的 packet list。Level 4 Release-gated Autonomy 应映射为 owner gates，
而不是 execution scope。Q5 不是强制提问，operating intensity 也不是 state v2 field。
历史 mapping 可参考 [autonomy-levels.md](autonomy-levels.md) 与
[operating-intensity.md](operating-intensity.md)，但不要在新 state 中记录 legacy 术语。

请把现有 evidence/claim 表中的 owner-acceptance 行保留为历史记录。下次修改某项
decision 时，为它选择一个 durable decision record，并把其他可变 acceptance field
改为指向该记录的 link；无需批量重写。
