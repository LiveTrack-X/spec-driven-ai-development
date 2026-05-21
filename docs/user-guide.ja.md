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

## トラブルシューティング FAQ

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
- [autonomy-levels.md](autonomy-levels.md): autonomy level と work packet
- [implementation-notes.md](implementation-notes.md): 実装判断の記録ルール
- [session-handoff.md](session-handoff.md): 長いセッションの handoff
