# SPEC-Driven AI Development

[English](README.md) | [한국어](README.ko.md) | [中文](README.zh.md) | [日本語](README.ja.md)

この文書は日本語の案内用 README です。このリポジトリの正本は英語の
[README.md](README.md)、`docs/`、`templates/`、`scripts/` です。内容が食い違う場合は英語の正本文書を優先してください。

## これは何か

SPEC-Driven AI Development は、AI コーディングエージェントを単なる実装ツールではなく、
計画、SPEC 作成、実装、レビュー、QA、ドキュメント保守の役割に分けて使うための
プロジェクト運営手法です。人間の Owner は方向性、リスク、優先順位、最終受け入れを管理します。

中心となる考え方：

- 人間の Owner が方向、優先順位、リスク許容度、最終判断を持つ。
- AI は計画、SPEC、実装、レビュー、検証、ドキュメント保守を支援する。
- SPEC は作業基準だが、完了の証拠はコード、テスト、文書、再現可能な結果で示す。
- 重要な変更は別の AI、モデル、セッション、または人間によるクロスレビューを受ける。
- 繰り返される問題は、ルール、チェックリスト、テスト、テンプレートに変換する。

## いつ使うか

次のようなプロジェクトに向いています。

- 複数の AI セッション、モデル、ツールが同じプロジェクトに関わる。
- Owner が直接コードを書かなくても、方向と品質を監督する必要がある。
- SPEC、過去文書、プロダクトメモ、handoff が増えている。
- AI の「完了」宣言を証拠で確認する必要がある。
- リリース、移行、セキュリティ、データ損失、ロールバックのリスクがある。

適合度は [docs/fit-assessment.md](docs/fit-assessment.md) で確認できます。

## クイックスタート

任意の AI コーディング環境で次のプロンプトから始められます。

```text
Use the SPEC-driven AI development workflow from this repository.
Start by clarifying the product pain, owner control model, active SPEC, non-goals, risks, and evidence required for completion.
```

詳細な kickoff プロンプトは [prompts/kickoff-prompt.md](prompts/kickoff-prompt.md) を参照してください。

## ツールアダプター

複数の AI コーディングツール向けにアダプターを用意しています。

- Codex: `AGENTS.md` + `ai-spec-project-start` skill
- Claude Code: `CLAUDE.md`
- Cursor: `.cursor/rules/spec-driven-ai-development.mdc`
- GitHub Copilot: `.github/copilot-instructions.md`
- 汎用 AI ツール: `AI-SESSION-INSTRUCTIONS.md`

詳しくは [docs/tool-adapters.md](docs/tool-adapters.md) を参照してください。

例：

```powershell
.\scripts\install-agent-adapter.ps1 -Adapter claude-code -TargetPath C:\path\to\project
```

## 中核ルール

Core 5:

- 現在の状態は過去の履歴より優先される。
- 証拠は AI の自信より優先される。
- アクティブな範囲は面白い将来アイデアより優先される。
- Owner の判断は AI の勢いより優先される。
- 繰り返される痛みはルール、チェックリスト、テスト、テンプレートになる。

全体のルールは [docs/implicit-rules.md](docs/implicit-rules.md) を参照してください。

## 主要ドキュメント

- [docs/pattern-catalog.md](docs/pattern-catalog.md): パターンカタログ
- [docs/anti-patterns.md](docs/anti-patterns.md): アンチパターン
- [docs/fit-assessment.md](docs/fit-assessment.md): 適合度評価
- [docs/diagrams.md](docs/diagrams.md): Mermaid 図
- [templates/project-control-files](templates/project-control-files): プロジェクト制御ファイルのテンプレート

## 検証

```bash
python scripts/validate_repo.py
```

## ライセンス

MIT。詳しくは [LICENSE](LICENSE) を参照してください。
