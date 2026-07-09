# SPEC-Driven AI Development

[English](README.md) | [한국어](README.ko.md) | [中文](README.zh.md) | [日本語](README.ja.md)

ステータス: `2.0.2` 安定ドキュメント/パッケージリリース。

有効性は project fit、Owner の運用規律、evidence quality に依存します。

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

## 状況別ガイド

詳しい FAQ と状況別の説明は [docs/user-guide.ja.md](docs/user-guide.ja.md) を参照してください。
短い判断基準は次のとおりです。

| 状況 | 推奨される開始点 |
|---|---|
| 一度きりの依頼で、後から継続しない | One-shot prompt |
| 小さな作業だが、evidence や短い handoff が必要 | Mini SDAD |
| 複数セッション、レビュー、TODO、review findings が必要 | Standard SDAD |
| release、migration、production、user data、auth、money、security、rollback リスクがある | Full SDAD または明示的 gate を持つ Standard 以上 |
| Claude.ai や ChatGPT web のように project files を編集できない chat-only 環境 | 計画だけを行い、adapter をインストールしたと主張しない |
| AI が "done" と言った | 変更ファイル、確認証拠、docs checked、制限、Owner acceptance を確認する |
| 正しい SDAD command や skill 名が分からない | 自然言語で依頼し、AI が review、implementation、release、docs、handoff、autonomy tuning intent に route する |
| SPEC にない実装判断が発生した | `docs/implementation-notes.md` に assumption、compromise、tradeoff、follow-up を記録する |

## トラブルシューティング FAQ

- Q. 正しい SDAD command や skill 名が分かりません。
  A. 自然言語で依頼してください。例: "問題がないか見て"、"SPEC に従って実装して"、
  "release 準備をして"、"README を分かりやすくして"、"handoff を作って"。
  AI は interpreted intent、SDAD scale/intensity、autonomy level、evidence、
  owner gate を最初に短く述べます。
- Q. AI が頻繁に承認を求める、または先に進みすぎる。
  A. autonomy level と packet 境界を一緒に調整します。
  - Level 0 Ask-first: 新しい、曖昧、またはリスクのある setup で各段階を確認します。
  - Level 1 Unit Autonomy: 1 つの review-worthy unit だけを完了し、証拠とともに停止します。
  - Level 2 Work Packet Autonomy: 承認済み packet 内の関連 unit を続けて進めます。
  - Level 3 Session Autonomy: 低リスクの session goal、time box、stop condition まで進めます。
  - Level 4 Release-gated Autonomy: release、migration、destructive action、
    user data、auth、money、security、rollback、production claim では Owner gate を維持します。
- Q. AI が "done" とだけ言う。
  A. final done ではなく evidence-ready status を求めます。変更ファイル、
  checks、docs checked、制限や未検証項目、review findings、Owner decision
  needed を確認します。
- Q. SDAD の文書が多すぎる。
  A. One-shot または Mini SDAD を使うか、Standard/Full の operating intensity
  を下げます。維持できない control file は作らない方が安全です。
- Q. 次のセッションで文脈を失いやすい。
  A. `save-state.md` を更新するか、長いセッションを閉じる前に
  `docs/sdad/handoffs/YYYY-MM-DD-topic.md` を作成します。

## クイックスタート

初めて使う場合は、まず [docs/getting-started.md](docs/getting-started.md) を読んでください。
prompt-only の開始方法、ツールアダプターの導入、Codex skill の導入手順を分けて説明しています。

リポジトリを clone せずに始めたい場合は
[docs/no-clone-quick-install.md](docs/no-clone-quick-install.md) を使ってください。
AI エージェントへそのまま渡せるプロンプトと、コピー＆ペースト用のインストールコマンドがあります。
もっとも簡単な方法では、ターミナル、Git、Python は不要です。
小さなプロジェクトでは、まず [docs/mini-sdad.md](docs/mini-sdad.md) を使ってください。
複数セッション、再訪、レビュー、リリースやデータリスクが出たら full SDAD に拡張します。
単純な yes 数よりリスクを優先します。Q5 の production、migration、user data、auth、
money、release、rollback リスクが 1 つでもある場合は、少なくとも Standard を検討してください。
Standard/Full SDAD を選ぶ場合は、各ループの最後に SPEC、TODO、review findings を最新化する必要があります。
維持コストについては [docs/maintenance-cost.md](docs/maintenance-cost.md) を参照してください。
Standard/Full SDAD では、project scale とは別に operating intensity を選びます:
`Standard SDAD / High`, `Standard SDAD / Medium`, `Standard SDAD / Low`,
`Full SDAD / High`, `Full SDAD / Medium`, `Full SDAD / Low`。
Q5 project だからといって、すべての packet が High になるわけではありません。
Q5 gate の挙動、ポリシー、境界、証拠上の主張、リスク受け入れを変える
packet だけを `Full SDAD / High` に上げます。usable baseline ができた後は
Medium または Low に下げ、evidence と owner review を圧縮します。詳しくは
[docs/operating-intensity.md](docs/operating-intensity.md) を参照してください。
Harness optimization、self-improving loop、retrieval/memory tuning、反復評価の
自動化のような advanced extension は、標準ループではありません。反復する
task unit、測定可能な metric、固定された model/tool surface、leakage risk、
具体的な budget、owner adoption gate がある場合だけ使用してください。
`save-state.md` を使うプロジェクトでは、セッション終了や中断、handoff、Owner の方向変更、
部分的または未検証の状態、次のセッションで文脈の再構築が難しい場合にも更新してください。
Mini SDAD にも完了ゲートがあります。変更ファイル、確認証拠、制限や未検証項目、
Owner の受け入れが示されるまでは done と見なしません。
ただし、すべての小さな作業ごとに停止する必要はありません。レビューする意味のある
開発単位を定義し、その範囲内の関連する小タスクは AI が続けて進め、証拠とともに handoff します。
Claude.ai や ChatGPT web のようなプロジェクトファイルシステムを持たない chat-only 環境では、
adapter をインストールしたと主張してはいけません。計画だけを行い、実際の導入は
プロジェクトファイルを編集できる AI coding tool で行ってください。

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
- 計画が曖昧な場合は、まずリポジトリ上の証拠を確認し、残った
  blocking question だけを推奨回答つきで Owner に尋ねる。

全体のルールは [docs/implicit-rules.md](docs/implicit-rules.md) を参照してください。

## 主要ドキュメント

- [docs/pattern-catalog.md](docs/pattern-catalog.md): パターンカタログ
- [docs/user-guide.ja.md](docs/user-guide.ja.md): 状況別ユーザーガイドと FAQ
- [docs/anti-patterns.md](docs/anti-patterns.md): アンチパターン
- [docs/fit-assessment.md](docs/fit-assessment.md): 適合度評価
- [docs/maintenance-cost.md](docs/maintenance-cost.md): 制御ファイルの維持コスト
- [docs/operating-intensity.md](docs/operating-intensity.md): Standard/Full の operating intensity
- [docs/session-handoff.md](docs/session-handoff.md): 長いセッションの handoff と文脈継続
- [docs/implementation-notes.md](docs/implementation-notes.md): SPEC に書かれていない実装判断の記録
- [docs/field-notes/repository-control-surface-method.md](docs/field-notes/repository-control-surface-method.md): guidance、enforcement、隔離、reviewed memory の制御面
- [docs/field-notes/cost-aware-agent-routing-method.md](docs/field-notes/cost-aware-agent-routing-method.md): advisor、worker、loop、コスト、証拠のルーティング
- [docs/diagrams.md](docs/diagrams.md): Mermaid 図
- [templates/project-control-files](templates/project-control-files): プロジェクト制御ファイルのテンプレート

## 検証

```bash
python scripts/validate_repo.py
```

## ライセンス

MIT。詳しくは [LICENSE](LICENSE) を参照してください。
