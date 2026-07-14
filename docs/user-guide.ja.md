# ユーザーガイドと FAQ

[English](user-guide.md) | [한국어](user-guide.ko.md) | [中文](user-guide.zh.md) | [日本語](user-guide.ja.md)

この文書は日本語の案内用です。英語の [user-guide.md](user-guide.md)、`docs/`、
`templates/`、`scripts/` が英語の正本文書です。内容が異なる場合は英語の正本を優先します。

SDAD Protocol（SPEC-Directed AI Development）は、AI 支援開発のための
repository-local な運用プロトコルです。実装手法や AI ツールを規定せず、現在の
scope、validation、evidence、unresolved state、Owner authority を一貫して維持します。
AI の正しさを保証したり、tests、CI、permissions、review を置き換えたりはしません。

## 最初に区別する 3 つの軸

> Scale は維持する control files、`execution_scope` は AI が今どこまで進めるか、
> owner gate はどの操作で必ず停止するかを決めます。

| 軸 | 管理するもの | 管理しないもの |
|---|---|---|
| Scale | 維持する control surface | 作業の許可範囲 |
| `execution_scope` | `unit` または `packet` の実行境界 | risk acceptance |
| owner gate | 保護対象アクションの権限 | 実装品質 |
| validation contract | 検査と証明の範囲 | owner acceptance |
| handoff | セッション間の復元ポインタ | 現在の source of truth |

## 早見表

| 状況 | Scale | 既定値 |
|---|---|---|
| 現在の依頼だけを処理し、永続ファイルが不要 | One-shot | 現在の依頼、SDAD file なし |
| 小さな feature または bug fix | Mini | `execution_scope: unit` |
| 複数セッション、review、TODO、継続 state が必要 | Standard | `execution_scope: packet` |
| release、migration、security、data、production risk がある | Full | `execution_scope: packet` + 必要な owner gates |

通常、ユーザーは goal だけを伝えれば十分です。AI は repository と依頼を根拠に先に推論し、
不明点が Scale や owner gate を実質的に変える場合だけ、推奨案を添えた blocking question を
1 つ行います。

推奨される解釈レポート:

```text
Scale: Standard
Execution scope: packet
Reason: multi-session state and review findings already exist.
Owner gates: release only
Unresolved question: none
```

## 自然言語リクエスト

正しい SDAD command や skill 名を覚える必要はありません。

| このように依頼する | AI が解釈する intent |
|---|---|
| 「全体を確認して問題を探して」 | review/audit intent |
| 「現在の SPEC に従って実装して」 | implementation intent |
| 「release の前で止まって」 | release owner gate を持つ packet |
| 「次のセッションが続けられるようにして」 | handoff intent |
| 「この repo から採用できるものを探して」 | reference-intake intent |
| 「承認要求が多すぎる」 | `execution_scope` と owner-gate の承認・失効調整 intent |
| 「commit and wait」 | commit で停止。push/release/deploy の権限ではない |

"carefully"、"fully"、"quickly" などの修飾語は review depth や圧縮度を変えるだけで、
scope を拡張しません。`evidence-ready` も Owner が受け入れるまでは最終完了ではありません。

## 1 つの作業ループ

1. Plan — goal、scope、acceptance、evidence、gate を定義します。
2. Route — adapter、state、INDEX に従い、必要な文書だけを選びます。
3. Implement — 小さく review 可能な unit で変更します。
4. Verify — validation を実行し、結果と限界を集めます。
5. Report — evidence-ready report を提出します。

Owner Gate は保護対象アクションがある場合、Handoff はセッション継続が必要な場合だけ使う
条件付き checkpoint です。毎 packet の必須追加ステップにはしません。

## Context を読む順序

Standard/Full の開始時は次の順序を使います。

```text
tool adapter -> sdad-state.yaml -> docs/INDEX.md -> current source/tests -> selected routed docs
```

`routed_docs` は現在の packet で選択可能な文書の集合であり、startup 時にすべて読む命令では
ありません。現在の intent に必要な文書だけを開き、final report には実際に読んだ path だけを
記録します。archive、大きな log、generated report、private data は既定 context に入れません。

大きな Copy-Paste/bootstrap prompt は、インストールまたはアップグレード時に一度だけ使います。
導入後は毎回読み直したり貼り直したりせず、adapter -> state -> INDEX に従います。

ツール固有の native session、checkpoint、doctor 機能は convenience または tool diagnostics です。
SDAD の `sdad-state.yaml`、`current_handoff`、Doctor report を置き換えません。

## State と handoff

state v2 では `current_handoff` が唯一の任意の現在継続性ポインタです。値がある場合、文書の
packet marker は active packet と一致する必要があります。長い内容を handoff に複製せず、
SPEC、TODO、findings、ADR、evidence の path と次の action を結びます。

`save-state.md` は v3.1 migration 時だけ読む legacy input です。v2 への移行後、第 2 の現在 state
として更新し続けません。新しい handoff は必要な場合だけ
`docs/sdad/handoffs/YYYY-MM-DD-HNNNN-topic.md` に作成します。`HNNNN` は端末時刻ではなく
リポジトリの論理順序であり、日付は説明用です。既存の番号なし handoff は維持し、現在性は
`current_handoff` だけで決定します。

## Owner gate の承認を再利用する

条件付き承認は次の exact field で記録できます。

```text
Decision:
Authorized action:
Packet:
Conditions:
Expires when:
Evidence required before action:
```

`Authorized action`、`Packet`、`Conditions`、`Evidence required before action` が変わらず、
承認後に source が変更されず、`Expires when` に到達していなければ、同じ承認を再度
求めません。いずれかが変わると承認は失効し、Owner の新しい判断が必要です。

## 1 つの事実は 1 か所に記録する

| 内容 | 正本の場所 |
|---|---|
| requirements と acceptance の変更 | SPEC |
| 小さな SPEC 外の実装判断 | `docs/implementation-notes.md` |
| 戻しにくい構造判断 | ADR |
| 未解決の作業 | TODO または finding |
| 次セッションの復元情報 | handoff |
| 現在の実行 state | `sdad-state.yaml` |

handoff は上記文書の内容を複製せず、path と重要な結果だけを結びます。

## Evidence と主張の限界

| evidence | 言えること | 言えないこと |
|---|---|---|
| Doctor green | 宣言された構造が整合している | 機能の正確性、効果、Owner acceptance |
| task benchmark 成功 | 特定 task が成功した | 全体として以前より優れている |
| controlled comparison 成功 | 比較条件で改善した | 他の条件にも自動で当てはまる |

AI が done とだけ言う場合、changed files、checks、docs checked、limits、
partial/degraded/unverified behavior、open findings、必要な Owner decision を含む
`evidence-ready` report を求めてください。`owner-accepted` は別の状態です。

## トラブルシューティング FAQ

### AI が repository を確認する前に質問する

まず code、tests、active docs、SPEC、TODO、findings、ADR を確認させます。その後も Scale や
gate を変える不明点がある場合だけ、推奨案を添えた質問を 1 つ許可します。

### 承認要求が多すぎる、または AI が進みすぎる

`execution_scope` が `unit | packet` のどちらかを確認してください。micro-task をまとめて処理する
場合は `packet` を使います。複数 packet の連続実行には、Owner が packet list を持つ plan を
明示的に承認する必要があります。時間境界の session は実行範囲の値ではありません。

### SDAD file が多すぎる

継続性が不要なら One-shot、小さな作業なら Mini を選びます。Standard/Full でも
`routed_docs` をすべて読まず、現在の intent に必要なものだけを選びます。

### formal test がない

利用可能な最も強い practical evidence を使い、限界を明示します。build/lint/typecheck、
targeted script、smoke test、API response、log、screenshot、manual reproduction、docs diff などです。

### chat-only tool がインストール済みだと言う

project filesystem を編集できなければインストール済みではありません。Claude.ai や
ChatGPT web では planning だけを行い、実際の adapter 導入は coding tool で実施します。

## 次に読む文書

- [getting-started.md](getting-started.md): インストールと最初の実行
- [no-clone-quick-install.md](no-clone-quick-install.md): clone なしの one-time bootstrap
- [mini-sdad.md](mini-sdad.md): 小規模 project
- [owners-guide.md](owners-guide.md): Owner 運用
- [ai-work-loop.md](ai-work-loop.md): 作業ループ
- [session-handoff.md](session-handoff.md): handoff contract
- [implementation-notes.md](implementation-notes.md): 実装判断の記録

## v3.1 の用語を使っていた場合

この節は migration/history 専用です。Level 0 Ask-first は未承認状態、Level 1 Unit Autonomy は
`unit`、Level 2 Work Packet Autonomy は `packet` と解釈できます。Level 3 Session Autonomy は
session を scope にせず、承認済み packet list で表現します。Level 4 Release-gated Autonomy は
execution scope ではなく owner gates へ移します。Q5 は必須質問ではなく、operating intensity も
state v2 field ではありません。過去の mapping は [autonomy-levels.md](autonomy-levels.md) と
[operating-intensity.md](operating-intensity.md) を参照できますが、新しい state に legacy 用語を
記録しないでください。
