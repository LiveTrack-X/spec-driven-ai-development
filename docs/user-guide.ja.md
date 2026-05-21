# ユーザーガイドと FAQ

[English](user-guide.md) | [한국어](user-guide.ko.md) | [中文](user-guide.zh.md) | [日本語](user-guide.ja.md)

この文書は日本語の案内用 user guide です。正本は英語の
[user-guide.md](user-guide.md)、`docs/`、`templates/`、`scripts` です。
内容が食い違う場合は英語の正本文書を優先してください。

SDAD は AI-assisted development のための制御方法です。AI の出力を自動的に
正しくするものではありませんが、scope、evidence、review、handoff、owner
acceptance を失いにくくします。

## 早見表

| 状況 | 使うもの | 期待すること |
|---|---|---|
| 一度きりの依頼 | One-shot prompt | SDAD files は作らない |
| 小さな作業だが done の証拠が必要 | Mini SDAD | AI instruction file 1 つ |
| 複数セッション、レビュー、TODO が続く | Standard SDAD | SPEC、TODO、review、docs control files |
| release、migration、production、user data、auth、money、security、destructive action、rollback リスクがある | Full SDAD または明示的 gate を持つ Standard 以上 | review、evidence、必要な ADR、owner gate |
| Claude.ai や ChatGPT web などの chat-only 環境 | planning only | adapter をインストールしたと主張しない |

プロジェクトを守れる最小の scale を選びます。risk は単純な yes 数より優先されます。

## SDAD が追加するもの

- 古いメモが active work を上書きしないよう、現在の SPEC を基準にする。
- work packet により、すべての micro-task で停止しない。
- review-worthy unit により、evidence をレビュー可能な単位にまとめる。
- AI の "done" と owner-accepted を分ける。
- SPEC にない実装判断を `docs/implementation-notes.md` に残す。
- `save-state.md` と handoff により、次のセッションが repo state から続けられる。
- 大きな logs、archives、generated files、private data が AI context に入るのを防ぐ。
- context layer により、今読むもの、必要時に読むもの、bounded evidence として参照するものを分ける。
- before/after change guard により、autonomy の結果を監査可能にする。

## SDAD が context を分ける方法

| layer | 例 | 使い方 |
|---|---|---|
| always-loaded instructions | `AGENTS.md`, `CLAUDE.md`, Cursor/Copilot rules | 毎回読めるよう短く、現在有効な状態にします。 |
| active control files | 現在の SPEC、TODO、review findings、implementation notes、save-state | 現在の packet に必要な部分を読みます。 |
| on-demand references | pattern catalog、anti-patterns、field notes、localized guides | 現在の問いに必要なときだけ開きます。 |
| archive and evidence | 古い handoff、logs、generated reports、historical notes | path または bounded read で参照し、chat に丸ごと貼りません。 |

AI が迷った場合、まず active packet、source of truth、足りない evidence を
説明させ、履歴を大量に読ませることから始めないでください。

## 自然言語リクエスト

ユーザーは SDAD 用語、adapter 名、skill 名を覚える必要はありません。普通の
言葉で依頼してください。AI は intent を推測し、scope、evidence、owner gate
を守る最小の SDAD route を選び、どう解釈したかを短く説明します。

| このように言った場合 | AI の解釈 |
|---|---|
| "全体を見て", "問題がないか確認して", "bug を探して" | review または audit intent |
| "実装して", "修正して", "SPEC に合わせて" | SPEC implementation intent |
| "release して", "publish して", "tag を切って" | Level 4 owner gate 付き release intent |
| "docs が分かりにくい", "guide を書いて", "FAQ を追加して" | documentation intent |
| "あとで続けられるように", "handoff して" | handoff または save-state intent |
| "この repo から借りられるものはある?" | reference-intake intent |
| "approval request が多すぎる", "先に進みすぎる" | autonomy tuning intent |

intent が明確なら AI は進めて構いません。複数の intent が衝突して scope や
risk が変わる場合だけ、推奨デフォルト付きで blocking question を 1 つだけ
聞きます。

## トラブルシューティング FAQ

### Q. 正しい SDAD command や skill 名が分かりません。

A. 自然言語で依頼し、AI に intent を route させてください。

例:

- "この repo で問題になりそうな箇所を確認して。"
- "現在の SPEC に従って実装し、SPEC にない判断は implementation notes に残して。"
- "approval request が多すぎる。この packet の autonomy level を調整して。"
- "release 準備をして。ただし release と rollback decision は owner gate にして。"
- "初めてのユーザーに分かりやすい README にして。"
- "次の session が続けられるように handoff を作って。"

AI は interpreted intent、SDAD scale/intensity、autonomy level、必要な
evidence、owner gate を最初に短く述べます。その解釈が risk や scope を
変える場合は、続行前に clarification question を 1 つだけ聞きます。

### Q. AI が頻繁に承認を求める、または先に進みすぎる。

A. autonomy level、packet boundary、operating intensity を一緒に調整します。

| 症状 | 試すこと | 意味 |
|---|---|---|
| 小さなステップごとに聞く | Level 2 Work Packet Autonomy | packet 境界を承認し、その中の micro-task は AI が続けて処理します。 |
| 1 unit だけ終えて止まればよい | Level 1 Unit Autonomy | 1 つの review-worthy unit が承認済み packet です。 |
| setup が新しい、曖昧、または危険 | Level 0 Ask-first | 境界が明確になるまで意味のある各ステップで確認します。 |
| 低リスクの session goal が明確 | Level 3 Session Autonomy | session goal、time box、stop condition まで進めます。 |
| release、migration、destructive action、user data、auth、money、security、rollback、production claim がある | Level 4 Release-gated Autonomy | AI は準備できますが、risk acceptance と release decision は owner gate を維持します。 |

### Q. AI が repository を確認する前に質問する。

A. clarification checkpoint を要求します。

```text
Inspect repository evidence first: code, tests, active docs, SPEC, TODOs, review
findings, and ADRs. Ask only the next blocking question, include your
recommended answer, and explain what changes if I choose differently.
```

### Q. AI が "done" とだけ言い、何が変わったかわからない。

A. final completion ではなく evidence-ready status を求めます。

確認するもの:

- changed files,
- tests/build/lint/manual check または実行できなかった理由,
- docs checked または updated,
- 必要な implementation notes,
- review findings の処理または追跡,
- limitations、partial/degraded/unverified behavior,
- まだ必要な owner decision.

### Q. SDAD のファイルが多すぎる。

A. より小さい scale、または低い intensity を使います。

一度きりの作業は One-shot prompt、証拠が必要な小さな作業は Mini SDAD を使います。
Standard/Full は control file を維持できる場合だけ使ってください。

### Q. タスクの大きさがわからない。

A. 予想コード行数だけでなく continuity と risk で分類します。

| サイン | 使うもの |
|---|---|
| 一度きりの回答、文言修正、将来の文脈が不要な小変更 | One-shot prompt |
| 小変更だが done の証拠が必要 | Mini SDAD または Level 1 Unit Autonomy |
| 関連する docs、prompt、template、code 更新 | Standard SDAD + Level 2 Work Packet Autonomy |
| 複数ファイル behavior change、反復 bug、review findings、context loss | Standard SDAD / Medium または High |
| release、migration、destructive action、production claim、real user data、auth、money、security、rollback | Full SDAD または Level 4 gate 付き Standard 以上 |

### Q. ファイル変更の前後に何を確認する？

A. 軽い before/after change guard を使います。

変更前に active SPEC、work packet、autonomy level、allowed scope、non-goals、
owner gate、stop condition を確認します。

変更後に changed files、checks run、docs checked/updated、implementation notes
の要否、limitations、unverified behavior、owner decision を報告させます。

### Q. formal test がない場合、どの evidence で足りる？

A. その時点で可能な最も強い practical evidence を使い、限界を明示します。

例: build/lint/typecheck output、targeted script、smoke test steps、curl/API
response、application logs、screenshot、manual reproduction note、docs diff、
unverified behavior の一覧。

### Q. 次のセッションで文脈を失いやすい。

A. セッション終了前に `save-state.md` を更新するか handoff を作成します。

長いセッションを閉じる、または新しいセッションへ渡す前に
`docs/sdad/handoffs/YYYY-MM-DD-topic.md` を作成し、長い内容は複製せず、
SPEC、TODO、ADR、review findings、implementation notes、evidence path をリンクします。

### Q. SPEC にない実装判断が必要。

A. 判断を見える場所に残します。

通常の実装判断は `docs/implementation-notes.md` に assumption、compromise、
rejected alternative、tradeoff、follow-up、verification impact として記録します。
戻しにくく、将来の保守者が驚く real tradeoff だけを ADR にします。

### Q. review で bug が見つかった。

A. evidence-ready は reviewable であり、owner-accepted ではありません。

同じ packet で直せるなら直します。そうでなければ `review-findings.md` または
`docs/TODO-Open-Items.md` に移し、次の packet を定義します。

### Q. chat-only tool が SDAD をインストールしたと言う。

A. project filesystem を編集できなければ、インストール済みではありません。

Claude.ai や ChatGPT web は planning には使えますが、adapter file を保存したと
主張してはいけません。実際の導入は Codex、Claude Code、Cursor、Copilot Chat など
project folder を編集できる AI coding tool で行います。

### Q. release、data、auth、money、security、destructive work に触れる。

A. autonomy を上げるだけで解決しないでください。

Standard または Full SDAD で明示的 gate を置き、risk acceptance、rollback posture、
production claim、migration、destructive action、real user data handling は owner
approval を維持します。

## 次に読む文書

- [getting-started.md](getting-started.md): setup path と最初の 10 分
- [no-clone-quick-install.md](no-clone-quick-install.md): clone なしで始める
- [mini-sdad.md](mini-sdad.md): 小さなプロジェクト向け one-file SDAD
- [context-stability.md](context-stability.md): context layer と bounded read
- [autonomy-levels.md](autonomy-levels.md): autonomy level と work packet
- [implementation-notes.md](implementation-notes.md): 実装判断の記録ルール
- [session-handoff.md](session-handoff.md): 長いセッションの handoff
