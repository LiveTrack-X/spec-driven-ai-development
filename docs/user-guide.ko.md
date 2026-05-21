# 사용자 가이드와 FAQ

[English](user-guide.md) | [한국어](user-guide.ko.md) | [中文](user-guide.zh.md) | [日本語](user-guide.ja.md)

이 문서는 한국어 안내용 user guide입니다. 기준 문서는 영어
[user-guide.md](user-guide.md), 영어 기반 `docs/`, `templates/`, `scripts`입니다.
내용이 다르면 영어 기준 문서를 우선하세요.

SDAD는 AI 코딩을 위한 제어 방식입니다. AI 결과가 자동으로 맞아지는 것은
아니지만, scope, evidence, review, handoff, owner acceptance를 잃어버리기
어렵게 만듭니다.

## 빠른 선택

| 상황 | 사용 | 기대할 것 |
|---|---|---|
| 한 번만 처리할 요청이다 | One-shot prompt | SDAD 파일을 만들지 않음 |
| 작은 작업이지만 done의 증거가 필요하다 | Mini SDAD | AI instruction file 하나 |
| 여러 세션, 리뷰, TODO가 이어진다 | Standard SDAD | SPEC, TODO, review, docs control files |
| release, migration, production, user data, auth, money, security, destructive action, rollback 위험이 있다 | Full SDAD 또는 명시적 gate가 있는 Standard 이상 | review, evidence, 필요 시 ADR, owner gate |
| Claude.ai, ChatGPT web 같은 chat-only 환경이다 | planning only | adapter 설치를 주장하지 않음 |

프로젝트를 보호할 수 있는 가장 작은 scale을 고르세요. risk는 단순 yes 개수보다
우선합니다.

## SDAD가 해주는 일

- 현재 SPEC을 기준으로 삼아 오래된 노트가 active work를 덮어쓰지 않게 합니다.
- work packet으로 모든 micro-task마다 멈추지 않게 합니다.
- review-worthy unit으로 evidence를 검토 가능한 단위로 묶습니다.
- AI가 "done"이라고 말해도 evidence-ready와 owner-accepted를 구분합니다.
- SPEC에 없던 구현 판단을 `docs/implementation-notes.md`에 남깁니다.
- `save-state.md`와 handoff로 다음 세션이 repo state에서 이어가게 합니다.
- 큰 로그, archive, generated file, private data가 AI context를 오염시키지 않게 합니다.

## 문제 해결 FAQ

### Q. AI가 너무 자주 승인 요청하거나 너무 앞서 나가요.

A. autonomy level, packet boundary, operating intensity를 같이 조정하세요.

| 증상 | 시도 | 의미 |
|---|---|---|
| 작은 단계마다 묻는다 | Level 2 Work Packet Autonomy | packet 경계를 승인하고, 안의 micro-task는 AI가 이어서 처리합니다. |
| 한 unit만 끝내고 멈추면 된다 | Level 1 Unit Autonomy | review-worthy unit 하나가 승인된 packet입니다. |
| setup이 새롭거나 애매하거나 위험하다 | Level 0 Ask-first | 경계가 분명해질 때까지 의미 있는 단계마다 묻습니다. |
| 저위험 session goal이 분명하다 | Level 3 Session Autonomy | session goal, time box, stop condition까지 진행합니다. |
| release, migration, destructive action, user data, auth, money, security, rollback, production claim이 있다 | Level 4 Release-gated Autonomy | AI는 준비할 수 있지만 risk acceptance와 release decision은 owner gate를 유지합니다. |

### Q. AI가 질문부터 하고 repository를 확인하지 않아요.

A. clarification checkpoint를 요구하세요.

```text
Inspect repository evidence first: code, tests, active docs, SPEC, TODOs, review
findings, and ADRs. Ask only the next blocking question, include your
recommended answer, and explain what changes if I choose differently.
```

### Q. AI가 "done"이라고만 말해서 뭘 했는지 모르겠어요.

A. final completion이 아니라 evidence-ready status를 요구하세요.

확인할 것:

- changed files,
- tests/build/lint/manual check 또는 실행하지 못한 이유,
- docs checked 또는 updated,
- 필요한 implementation notes,
- review findings 처리 또는 추적 여부,
- limitations, partial/degraded/unverified behavior,
- 아직 필요한 owner decision.

### Q. SDAD가 파일을 너무 많이 만드는 것 같아요.

A. 더 작은 scale이나 낮은 intensity를 쓰세요.

한 번만 할 일은 One-shot prompt, 작은 일이지만 evidence가 필요하면 Mini SDAD를
쓰세요. Standard/Full은 control file을 계속 유지할 수 있을 때만 사용하세요.

### Q. 다음 세션에서 맥락을 자꾸 잃어요.

A. 세션 종료 전에 `save-state.md`를 갱신하거나 handoff를 만드세요.

긴 세션을 닫거나 새 세션으로 넘기기 전에는
`docs/sdad/handoffs/YYYY-MM-DD-topic.md`를 만들고, 긴 내용은 복사하지 말고
SPEC, TODO, ADR, review findings, implementation notes, evidence path를 링크하세요.

### Q. SPEC에 없는 구현 판단이 필요해요.

A. 결정을 보이게 남기세요.

일반 구현 판단은 `docs/implementation-notes.md`에 assumption, compromise,
rejected alternative, tradeoff, follow-up, verification impact를 기록합니다.
되돌리기 어렵고 미래 유지보수자가 놀랄 real tradeoff만 ADR로 남깁니다.

### Q. review에서 bug가 나왔어요.

A. evidence-ready는 reviewable 상태이지 owner-accepted가 아닙니다.

같은 packet 안에서 고칠 수 있으면 고치고, 아니면 `review-findings.md` 또는
`docs/TODO-Open-Items.md`에 넣고 다음 packet을 정의하세요.

### Q. chat-only 도구가 SDAD를 설치했다고 말해요.

A. 프로젝트 파일 시스템을 편집할 수 없다면 설치한 것이 아닙니다.

Claude.ai, ChatGPT web 같은 브라우저 chat은 planning에는 쓸 수 있지만 adapter
file을 저장했다고 주장하면 안 됩니다. 실제 설치는 Codex, Claude Code, Cursor,
Copilot Chat 등 project folder를 편집할 수 있는 AI coding tool에서 하세요.

### Q. release, data, auth, money, security, destructive work를 건드려요.

A. autonomy를 올리는 것으로 해결하지 마세요.

Standard 또는 Full SDAD에서 명시적 gate를 두고, risk acceptance, rollback posture,
production claim, migration, destructive action, real user data handling은 owner
approval을 유지하세요.

## 다음으로 볼 문서

- [getting-started.md](getting-started.md): 설치 경로와 첫 10분
- [no-clone-quick-install.md](no-clone-quick-install.md): clone 없이 시작
- [mini-sdad.md](mini-sdad.md): 작은 프로젝트용 one-file SDAD
- [autonomy-levels.md](autonomy-levels.md): autonomy level과 work packet
- [implementation-notes.md](implementation-notes.md): 구현 판단 기록 규칙
- [session-handoff.md](session-handoff.md): 긴 세션 handoff
