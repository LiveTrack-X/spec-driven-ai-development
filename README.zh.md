# SPEC-Driven AI Development

[English](README.md) | [한국어](README.ko.md) | [中文](README.zh.md) | [日本語](README.ja.md)

本文是中文导览版 README。本仓库的规范文档以英文为准，包括
[README.md](README.md)、`docs/`、`templates/` 和 `scripts/`。如果本导览与英文文档不一致，请以英文规范文档为准。

## 这是什么

SPEC-Driven AI Development 是一种面向 AI 编程代理的项目治理方法。它不是
“让 AI 按规格写代码”这么简单，而是把 AI 分成规划、SPEC 编写、实现、评审、QA
和文档维护等角色，同时由人类 Owner 保留方向、风险和最终验收权。

核心思想：

- 人类 Owner 决定方向、优先级、风险容忍度和最终验收。
- AI 协助规划、SPEC、实现、评审、验证和文档维护。
- SPEC 定义工作目标，但完成证据必须来自代码、测试、文档和可复现结果。
- 重要变更需要其他 AI、模型、会话或人工进行交叉评审。
- 重复出现的问题应转化为规则、清单、测试或模板。

## 什么时候使用

当项目出现以下情况时，本方法特别适合：

- 多个 AI 会话、模型或工具会持续参与同一项目。
- Owner 不一定直接写代码，但需要监督方向和质量。
- SPEC、历史文档、产品笔记和 handoff 文件开始变多。
- AI 声称完成，但缺少可验证证据。
- 项目存在发布、迁移、安全、数据丢失或回滚风险。

可使用 [docs/fit-assessment.md](docs/fit-assessment.md) 进行适配度评估。

## 快速开始

第一次使用时，请先阅读 [docs/getting-started.md](docs/getting-started.md)。
它分别说明 prompt-only 启动、工具适配器安装和 Codex skill 安装路径。

如果不想先 clone 仓库，请使用
[docs/no-clone-quick-install.md](docs/no-clone-quick-install.md)。
它提供可直接交给 AI 代理的提示词，以及可复制粘贴的一步安装命令。

在任意 AI 编程环境中使用：

```text
Use the SPEC-driven AI development workflow from this repository.
Start by clarifying the product pain, owner control model, active SPEC, non-goals, risks, and evidence required for completion.
```

完整启动提示见 [prompts/kickoff-prompt.md](prompts/kickoff-prompt.md)。

## 工具适配器

本仓库提供多种 AI 编程工具适配器：

- Codex: `AGENTS.md` + `ai-spec-project-start` skill
- Claude Code: `CLAUDE.md`
- Cursor: `.cursor/rules/spec-driven-ai-development.mdc`
- GitHub Copilot: `.github/copilot-instructions.md`
- 通用 AI 工具: `AI-SESSION-INSTRUCTIONS.md`

说明见 [docs/tool-adapters.md](docs/tool-adapters.md)。

示例：

```powershell
.\scripts\install-agent-adapter.ps1 -Adapter claude-code -TargetPath C:\path\to\project
```

## 核心规则

Core 5:

- 当前状态优先于历史内容。
- 证据优先于 AI 自信。
- 活跃范围优先于有趣的未来想法。
- Owner 决策优先于 AI 的推进惯性。
- 重复出现的问题应变成规则、清单、测试或模板。

完整规则见 [docs/implicit-rules.md](docs/implicit-rules.md)。

## 主要文档

- [docs/pattern-catalog.md](docs/pattern-catalog.md): 模式目录
- [docs/anti-patterns.md](docs/anti-patterns.md): 反模式
- [docs/fit-assessment.md](docs/fit-assessment.md): 适配度评估
- [docs/diagrams.md](docs/diagrams.md): Mermaid 图示
- [templates/project-control-files](templates/project-control-files): 项目控制文件模板

## 验证

```bash
python scripts/validate_repo.py
```

## 许可证

MIT。详见 [LICENSE](LICENSE)。
