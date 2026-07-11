# SDAD Protocol

[English](README.md) | [한국어](README.ko.md) | [中文](README.zh.md) | [日本語](README.ja.md)

状态：`3.1.0` 稳定文档/软件包版本。

实际效果取决于 project fit、Owner 的执行纪律与 evidence quality。

本文是中文导览版 README。英文 [README.md](README.md) 以及英文版 `docs/`、
`templates/`、`scripts/` 是规范来源。如有差异，以英文规范文档为准。

## 这是什么

SDAD Protocol（SPEC-Driven AI Development）是一套 repository-local 工作协议，
用于防止多个 AI 工具和会话之间的 state、scope、evidence、Owner 权限、decision 与
handoff 发生偏移。Markdown 记录权限与预期，但不会在技术上阻止工具操作；真正的
强制执行由 permissions、hooks、sandbox、branch protection 等运行环境负责。

核心区别如下：

- Scale 决定需要长期维护哪些 control surface。
- `execution_scope` 决定 AI 现在可以执行到哪里。
- owner gate 决定哪些受保护操作必须停下等待 Owner。
- validation contract 决定每项检查能证明什么、不能证明什么。
- `evidence-ready` 是可评审的 AI 结果，`owner-accepted` 是 Owner 的最终验收。

## 快速选择

AI 应先检查 repository 和请求，推断最小且安全的 Scale、`execution_scope` 与 owner gate。
只有在不确定项会实质改变判断时，才提出一个带推荐答案的问题。用户始终可以覆盖推断结果。

| Scale | 默认执行边界 | 默认控制 |
|---|---|---|
| One-shot | 当前请求 | 不创建持久 SDAD files |
| Mini | `unit` | 小任务所需的最小 instruction 与 evidence |
| Standard | `packet` | 持久 state、SPEC、TODO、review、validation |
| Full | `packet` | Standard + release/security/data 等具名 owner gates |

Scale 与风险权限相互独立。小任务的危险操作仍需 gate；选择 Full 也不会自动批准
受保护操作。

## 一个工作循环

所有 Scale 都使用同一个五步循环：

1. Plan — 定义 goal、scope、acceptance 与所需 evidence。
2. Route — 从 state 和 `docs/INDEX.md` 中只选择当前所需信息。
3. Implement — 以小而可评审的单元完成修改。
4. Verify — 运行 validation，收集结果与限制。
5. Report — 报告 evidence-ready 结果、risk 与未验证项。

Owner Gate 和 Handoff 不是永久追加的步骤，而是条件式 checkpoint。只有存在受保护
操作时才在 gate 停下；只有需要交给下一会话时才创建 handoff。

## Context 与连续性

Standard/Full 的启动路径是 tool adapter -> `sdad-state.yaml` -> `docs/INDEX.md`。
`routed_docs` 是当前 packet 可选择的文档集合，不是启动时全部读取的列表。Agent 只读取
当前 intent 所需的文档，并报告实际读取的路径。

在 state v2 中，`current_handoff` 是唯一可选的当前连续性指针。`save-state.md` 仅作为
v3.1 项目迁移时的 legacy migration input，不是当前 state 的第二个 source of truth。

大型 Copy-Paste/bootstrap prompt 只在安装或升级时使用一次。安装完成后的普通工作不应
每个会话重复粘贴它，而应遵循 adapter、state、INDEX。工具原生的
session/checkpoint/doctor 功能只是便利功能或 tool diagnostics，不能取代 SDAD state、
handoff 或 Doctor 的权威。

## Owner gate 与预先授权

为避免反复询问同一批准，可记录有条件的预先授权：

```text
Decision:
Authorized action:
Packet:
Conditions:
Expires when:
Evidence required before action:
```

授权只能在指定 packet 和条件内复用。批准后 source 发生变化、条件不再成立或达到
到期条件时，必须重新取得 Owner 决定。

## Evidence 与完成声明

- Doctor green：只确认结构和声明彼此一致。
- task benchmark 成功：证明指定 task 已成功。
- controlled comparison 成功：才可支持“实际优于旧方法”的声明。

不能只凭 Doctor 或 unit test 声称生产率提高、结果正确或已获 Owner 验收。AI 应提交
包含 changed files、checks、docs checked、limits、unverified items、open findings 的
`evidence-ready` report。最终完成需要 Owner 标记为 `owner-accepted`。

## 快速开始

首次使用请阅读 [docs/getting-started.md](docs/getting-started.md)。无需 clone 即可开始时，
使用 [docs/no-clone-quick-install.md](docs/no-clone-quick-install.md)；小型 project 使用
[docs/mini-sdad.md](docs/mini-sdad.md)。

详细中文说明和问题排查见 [docs/user-guide.zh.md](docs/user-guide.zh.md)，project fit 见
[docs/fit-assessment.md](docs/fit-assessment.md)，维护成本见
[docs/maintenance-cost.md](docs/maintenance-cost.md)。

各工具 adapter：

- Codex: `AGENTS.md` + `ai-spec-project-start` skill
- Claude Code: `CLAUDE.md`
- Cursor: `.cursor/rules/spec-driven-ai-development.mdc`
- GitHub Copilot: `.github/copilot-instructions.md`
- Generic AI tool: `AI-SESSION-INSTRUCTIONS.md`

在 Claude.ai、ChatGPT web 等不能编辑 project filesystem 的 chat-only 环境中，只能进行
planning，不能声称已安装 adapter。

## 问题排查 FAQ

- 不知道正确的 SDAD 命令或 skill 名称时，用自然语言请求。AI 应简短说明
  interpreted intent、Scale、`execution_scope`、evidence 和 owner gate。
- 批准请求过多时，检查是否为 `execution_scope: packet`。release 等受保护操作仍保留独立 gate。
- AI 只说 done 时，要求区分 `evidence-ready` report 与 Owner 验收。
- 下个会话丢失 context 时，检查 `current_handoff` 与 packet marker 是否一致。
- blocking 问题必须在先检查 repository evidence 后，限制为影响决策的一个问题。
- 在一个 packet 内连续处理有评审意义的开发单元，然后带 evidence 停下。

## 主要文档

- [docs/owners-guide.md](docs/owners-guide.md): Owner 快速采用指南
- [docs/ai-work-loop.md](docs/ai-work-loop.md): 单一执行循环
- [docs/session-handoff.md](docs/session-handoff.md): 条件式 handoff 与连续性
- [docs/implementation-notes.md](docs/implementation-notes.md): SPEC 之外的实现判断
- [docs/pattern-catalog.md](docs/pattern-catalog.md): pattern catalog

## 验证

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
git diff --check
```

## 从 v3.1 迁移

v3.1 的 Level 0 Ask-first、Level 1 Unit Autonomy、Level 2 Work Packet Autonomy、
Level 3 Session Autonomy、Level 4 Release-gated Autonomy 不是新的 state field。
请把执行边界映射为 `unit | packet`，把受保护权限映射为 owner gates。Q5 只是旧版的
风险推断表达，不是必问仪式。operating intensity 也已从 state v2 删除。
现有 `save-state.md`、[docs/operating-intensity.md](docs/operating-intensity.md)、
[docs/autonomy-levels.md](docs/autonomy-levels.md) 仅供 migration/history 参考。
不要把 Full SDAD / High 或 advanced extension 这类旧表达复制到新项目的执行合同中。

## 许可证

MIT。详见 [LICENSE](LICENSE)。
