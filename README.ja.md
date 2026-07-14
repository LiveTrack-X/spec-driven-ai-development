# SDAD Protocol

[English](README.md) | [한국어](README.ko.md) | [中文](README.zh.md) | [日本語](README.ja.md)

ステータス: `3.2.1` 安定ドキュメント/パッケージリリース。

有効性は project fit、Owner の運用規律、evidence quality に依存します。

この文書は日本語の案内用 README です。英語の [README.md](README.md)、
`docs/`、`templates/`、`scripts/` が正本です。内容が食い違う場合は英語の
正本文書を優先してください。

## これは何か

SDAD Protocol（SPEC-Directed AI Development）は、AI 支援開発のための
repository-local な運用プロトコルです。特定の実装手法を規定したり、エージェントを
実行したりせず、複数の AI ツールやセッションにわたって scope、validation、evidence、
unresolved state、Owner 権限を一貫して維持します。Markdown は権限と期待を記録しますが、
ツール利用を技術的に遮断するものではありません。実際の強制は permissions、hooks、
sandbox、branch protection などの実行環境が担います。

基本となる考え方は次のとおりです。

- Scale は、維持する control surface を決めます。
- `execution_scope` は、AI が今どこまで実行できるかを決めます。
- owner gate は、どの保護対象アクションで必ず停止するかを決めます。
- validation contract は、各検査が何を証明し、何を証明しないかを決めます。
- `evidence-ready` はレビュー可能な AI の結果、`owner-accepted` は Owner の最終受け入れです。

## 早見表

AI はまずリポジトリと依頼を調べ、最小で安全な Scale、`execution_scope`、owner gate を
推論します。判断を実質的に変える不明点が残る場合だけ、推奨案を添えて質問を 1 つ行います。
ユーザーは推論結果をいつでも上書きできます。

| Scale | 既定の実行境界 | 既定の制御 |
|---|---|---|
| One-shot | 現在の依頼 | 永続的な SDAD file なし |
| Mini | `unit` | 小さな作業向けの最小 instruction と evidence |
| Standard | `packet` | 継続 state、SPEC、TODO、review、validation |
| Full | `packet` | Standard + release/security/data など名前を明示した owner gates |

Scale とリスク権限は別です。小さな作業にも危険な操作には gate が必要で、
Full を選んでも保護対象アクションが自動承認されることはありません。

## 1 つの作業ループ

すべての Scale は、同じ 5 ステップのループを使います。

1. Plan — goal、scope、acceptance、必要な evidence を定義します。
2. Route — state と `docs/INDEX.md` から今必要な情報だけを選びます。
3. Implement — 小さくレビュー可能な単位で変更します。
4. Verify — validation を実行し、結果と限界を収集します。
5. Report — evidence-ready な結果、risk、未検証項目を報告します。

Owner Gate と Handoff は常設ステップではなく、条件付き checkpoint です。
保護対象アクションがあるときは gate で停止し、次のセッションへ渡す必要があるときだけ
handoff を作成します。

## Context と継続性

Standard/Full の開始経路は tool adapter -> `sdad-state.yaml` -> `docs/INDEX.md` です。
`routed_docs` は開始時に全件読むリストではなく、現在の packet で選択できる文書の集合です。
エージェントは intent に必要な文書だけを読み、実際に読んだ path を報告します。

state v2 では、`current_handoff` が唯一の任意の現在継続性ポインタです。
`save-state.md` は v3.1 プロジェクトの移行時だけ使う legacy migration input であり、
現在 state の第 2 の source of truth ではありません。

大きな Copy-Paste/bootstrap prompt は、インストールまたはアップグレード時に一度だけ使います。
導入後の通常作業では毎セッション貼り直さず、adapter、state、INDEX に従います。
ツール固有の session/checkpoint/doctor 機能は convenience または tool diagnostics であり、
SDAD state、handoff、Doctor の権威を置き換えません。

## Owner gate と事前承認

同じ承認を繰り返し求めないよう、条件付きの事前承認を記録できます。

```text
Decision:
Authorized action:
Packet:
Conditions:
Expires when:
Evidence required before action:
```

承認は `Authorized action`、`Packet`、`Conditions`、`Evidence required before action` が
変わらず、承認後に source が変更されず、`Expires when` に到達していない場合に限り
再利用します。いずれかが変われば、再び Owner の判断が必要です。

## Evidence と完了の主張

- Doctor green: 構造と宣言の整合性だけを確認します。
- task benchmark 成功: 指定した task の成功を示す evidence です。
- controlled comparison 成功: 以前の方法より実際に優れていると主張するための evidence です。

Doctor や unit test だけで、生産性向上、正確性、Owner acceptance を主張しません。
AI は changed files、checks、docs checked、limits、unverified items、open findings を含む
`evidence-ready` report を提出します。最終完了には Owner の `owner-accepted` が必要です。

## クイックスタート

最初に [docs/getting-started.md](docs/getting-started.md) を読んでください。clone せずに
始める場合は [docs/no-clone-quick-install.md](docs/no-clone-quick-install.md)、小規模な
project では [docs/mini-sdad.md](docs/mini-sdad.md) を使います。

詳しい日本語の説明とトラブルシューティングは [docs/user-guide.ja.md](docs/user-guide.ja.md)、
適合度は [docs/fit-assessment.md](docs/fit-assessment.md)、維持コストは
[docs/maintenance-cost.md](docs/maintenance-cost.md) を参照してください。

ツール別 adapter:

- Codex: `AGENTS.md` + `ai-spec-project-start` skill
- Claude Code: `CLAUDE.md`
- Cursor: `.cursor/rules/spec-driven-ai-development.mdc`
- GitHub Copilot: `.github/copilot-instructions.md`
- Generic AI tool: `AI-SESSION-INSTRUCTIONS.md`

Claude.ai や ChatGPT web のように project filesystem を編集できない chat-only 環境では
planning のみが可能で、adapter をインストールしたと主張してはいけません。

## トラブルシューティング FAQ

- 正しい SDAD command や skill 名が分からない場合は自然言語で依頼してください。AI は
  interpreted intent、Scale、`execution_scope`、evidence、owner gate を短く示します。
- 承認要求が多い場合は `execution_scope: packet` か確認します。release などの保護対象操作は
  別の gate として残します。
- AI が done とだけ言う場合は `evidence-ready` report と Owner の受け入れを区別させます。
- 次のセッションで context を失う場合は `current_handoff` と packet marker を確認します。
- blocking question は repository evidence を先に調べ、判断に必要な 1 問に限定します。
- 1 packet 内ではレビューする意味のある unit を続けて処理し、evidence とともに停止します。

## 主な文書

- [docs/owners-guide.md](docs/owners-guide.md): Owner 向けクイック導入ガイド
- [docs/ai-work-loop.md](docs/ai-work-loop.md): 単一の実行ループ
- [docs/session-handoff.md](docs/session-handoff.md): 条件付き handoff と継続性
- [docs/implementation-notes.md](docs/implementation-notes.md): SPEC 外の実装判断
- [docs/pattern-catalog.md](docs/pattern-catalog.md): pattern catalog

## 検証

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
git diff --check
```

## v3.1 から移行する場合

v3.1 の Level 0 Ask-first、Level 1 Unit Autonomy、Level 2 Work Packet Autonomy、
Level 3 Session Autonomy、Level 4 Release-gated Autonomy は新しい state field ではありません。
実行境界は `unit | packet`、保護権限は owner gates に分けてください。Q5 は必須質問ではなく、
リスク推論に使われた旧表現です。operating intensity も state v2 から削除されました。
既存の `save-state.md`、[docs/operating-intensity.md](docs/operating-intensity.md)、
[docs/autonomy-levels.md](docs/autonomy-levels.md) は migration/history 参照用です。
Full SDAD / High や advanced extension の表現を新規 project の実行契約へコピーしないでください。

## ライセンス

MIT。詳細は [LICENSE](LICENSE) を参照してください。
