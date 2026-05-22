# SPEC-Driven AI Development

[English](README.md) | [한국어](README.ko.md) | [中文](README.zh.md) | [日本語](README.ja.md)

상태: `1.1.7` 안정 문서/패키지 릴리즈.

효과는 프로젝트 적합도, 오너의 운영 규율, evidence 품질에 따라 달라집니다.

이 문서는 한국어 안내용 README입니다. 이 저장소의 기준 문서는 영어
[README.md](README.md)와 영어 기반 `docs/`, `templates/`, `scripts/`입니다.
내용이 다르면 영어 기준 문서를 우선하세요.

## 무엇인가

SPEC-Driven AI Development는 AI 에이전트를 단순 코딩 도구가 아니라
기획자, SPEC 작성자, 구현자, 리뷰어, QA 파트너, 문서 관리자로 나누어
사용하기 위한 프로젝트 운영 방식입니다.

핵심은 다음입니다.

- 인간 오너가 방향, 우선순위, 위험 허용치, 최종 수락을 결정한다.
- AI는 기획, SPEC, 구현, 리뷰, 검증, 문서화를 돕는다.
- SPEC은 작업 기준이지만 완료 증거는 코드, 테스트, 문서, 재현 가능한 결과다.
- 중요한 변경은 다른 AI, 모델, 세션, 또는 사람의 교차 검토를 받는다.
- 반복되는 불편함은 다음 프로젝트의 규칙, 체크리스트, 테스트, 템플릿으로 바꾼다.

## 언제 쓰나

다음에 해당하면 이 방식이 특히 잘 맞습니다.

- 여러 AI 세션이나 모델이 같은 프로젝트를 이어서 작업한다.
- 오너가 코드를 직접 많이 쓰지는 않지만 방향과 품질을 감독해야 한다.
- SPEC, 과거 문서, 제품 메모, handoff가 늘어나고 있다.
- AI가 "완료"라고 말해도 실제 근거를 확인하기 어렵다.
- 릴리즈, 마이그레이션, 보안, 데이터 손실, 롤백 위험이 있다.

적합도는 [docs/fit-assessment.md](docs/fit-assessment.md)를 사용해 점검하세요.

## 상황별 가이드

자세한 FAQ와 상황별 설명은 [docs/user-guide.ko.md](docs/user-guide.ko.md)를 보세요.
빠른 기준은 다음입니다.

| 상황 | 권장 시작점 |
|---|---|
| 한 번만 처리할 요청이고 나중에 이어갈 필요가 없다 | One-shot prompt |
| 작은 작업이지만 evidence나 짧은 handoff가 필요하다 | Mini SDAD |
| 여러 세션, 리뷰, TODO, review findings가 생긴다 | Standard SDAD |
| 릴리즈, 마이그레이션, production, user data, auth, money, security, rollback 위험이 있다 | Full SDAD 또는 명시적 gate가 있는 Standard 이상 |
| Claude.ai, ChatGPT web처럼 프로젝트 파일을 편집할 수 없는 chat-only 환경이다 | 계획만 하고 설치했다고 주장하지 않는다 |
| AI가 "done"이라고 말한다 | 변경 파일, 확인 증거, 문서 확인, 한계, 오너 수락 여부를 확인한다 |
| 정확한 SDAD command나 skill 이름을 모르겠다 | 자연어로 말하면 AI가 intent를 해석해 review, implementation, release, docs, handoff, autonomy 조정으로 route한다 |
| SPEC에 없던 구현 판단이 생겼다 | `docs/implementation-notes.md`에 가정, 타협, tradeoff, follow-up을 기록한다 |

## 문제 해결 FAQ

- Q. 정확한 SDAD 명령어나 skill 이름을 모르겠어요.
  A. 자연어로 요청하세요. 예: "문제 있는지 봐줘", "SPEC대로 구현해줘",
  "릴리즈 준비해줘", "README를 쉽게 고쳐줘", "handoff 만들어줘". AI는
  interpreted intent, SDAD scale/intensity, autonomy level, evidence, owner gate를
  먼저 짧게 밝혀야 합니다.
- Q. AI가 너무 자주 승인 요청하거나 너무 앞서 나가요.
  A. autonomy level과 packet 경계를 같이 조정하세요.
  - Level 0 Ask-first: 새롭거나 애매하거나 위험한 setup에서 단계마다 확인합니다.
  - Level 1 Unit Autonomy: 한 review-worthy unit만 끝내고 증거와 함께 멈춥니다.
  - Level 2 Work Packet Autonomy: 승인된 packet 안의 관련 unit들을 이어서 진행합니다.
  - Level 3 Session Autonomy: 저위험 session goal, time box, stop condition까지 진행합니다.
  - Level 4 Release-gated Autonomy: release, migration, destructive action,
    user data, auth, money, security, rollback, production claim은 오너 gate를 유지합니다.
- Q. AI가 "done"이라고만 말해요.
  A. final done이 아니라 evidence-ready 상태를 요구하세요. 변경 파일, checks,
  docs checked, 한계/미검증 항목, review findings, 오너 결정 필요사항을 확인합니다.
- Q. SDAD 문서가 너무 많게 느껴져요.
  A. One-shot 또는 Mini SDAD를 쓰거나 Standard/Full의 operating intensity를
  낮추세요. 유지할 수 없는 control file은 만들지 않는 편이 낫습니다.
- Q. 다음 세션에서 맥락을 자꾸 잃어요.
  A. `save-state.md`를 갱신하거나 긴 세션 종료 전
  `docs/sdad/handoffs/YYYY-MM-DD-topic.md`를 만드세요.

## 빠른 시작

처음 사용하는 경우 [docs/getting-started.md](docs/getting-started.md)를 먼저 보세요.
프롬프트만으로 시작하는 방법, 도구별 어댑터 설치, Codex skill 설치 경로를
나누어 설명합니다.

저장소를 클론하지 않고 시작하려면
[docs/no-clone-quick-install.md](docs/no-clone-quick-install.md)를 사용하세요.
AI 에이전트에게 그대로 넘길 프롬프트와 복사/붙여넣기 설치 명령이 있습니다.
가장 쉬운 경로는 터미널, Git, Python 없이도 시작할 수 있습니다.
작은 프로젝트라면 먼저 [docs/mini-sdad.md](docs/mini-sdad.md)를 사용하세요.
full SDAD는 여러 세션, 재방문, 리뷰, 릴리즈/데이터 위험이 생길 때 선택하면 됩니다.
단순 yes 개수보다 리스크가 우선합니다. Q5에 해당하는 production, migration,
user data, auth, money, release, rollback 위험이 하나라도 있으면 Standard 이상을
고려하세요.
Standard/Full SDAD를 선택하면 루프 끝마다 SPEC, TODO, review findings를 최신화해야 합니다.
비용 설명은 [docs/maintenance-cost.md](docs/maintenance-cost.md)를 보세요.
Standard/Full SDAD 안에서는 프로젝트 규모와 별도로 운영 강도를 고릅니다:
`Standard SDAD / High`, `Standard SDAD / Medium`, `Standard SDAD / Low`,
`Full SDAD / High`, `Full SDAD / Medium`, `Full SDAD / Low`.
Q5 프로젝트라고 모든 packet이 High가 되는 것은 아닙니다. Q5 gate의 동작,
정책, 경계, 증거 주장, 위험 수락을 바꾸는 packet만 `Full SDAD / High`로
올립니다. baseline이 생긴 뒤에는 Medium 또는 Low로 낮추고 evidence와
owner review를 압축하세요. 자세한 내용은
[docs/operating-intensity.md](docs/operating-intensity.md)를 보세요.
Harness optimization, self-improving loop, retrieval/memory tuning, 반복 평가
자동화 같은 고급 확장은 기본 루프가 아닙니다. 반복 task 단위, 측정 가능한
metric, 고정된 model/tool surface, leakage 위험, 구체적 budget, owner adoption
gate가 있을 때만 사용하세요.
`save-state.md`를 사용하는 프로젝트라면 세션 종료/중단, handoff, 오너 방향 변경,
부분/미검증 상태, 또는 다음 세션이 컨텍스트를 다시 구성하기 어려운 경우에도 최신화해야 합니다.
Mini SDAD도 완료 기준이 있습니다. 변경 파일, 확인 증거, 한계/미검증 항목,
오너 수락이 보이기 전에는 done으로 보지 않습니다.
다만 모든 작은 작업마다 멈추는 방식은 아닙니다. 리뷰 의미가 있는 개발 단위를 정하고,
그 안의 관련 작은 작업들은 AI가 이어서 진행한 뒤 증거와 함께 handoff해야 합니다.
Claude.ai나 ChatGPT 웹처럼 파일 시스템이 없는 chat-only 환경에서는 adapter를
설치했다고 말하면 안 됩니다. 이런 경우에는 계획만 하고, 실제 프로젝트 폴더를
편집할 수 있는 AI 코딩 도구에서 시작하세요.

아무 AI 코딩 도구에서 다음 프롬프트로 시작할 수 있습니다.

```text
Use the SPEC-driven AI development workflow from this repository.
Start by clarifying the product pain, owner control model, active SPEC, non-goals, risks, and evidence required for completion.
```

자세한 시작 프롬프트는 [prompts/kickoff-prompt.md](prompts/kickoff-prompt.md)를 참고하세요.

## 도구별 어댑터

Codex 외에도 여러 AI 코딩 도구에서 사용할 수 있습니다.

- Codex: `AGENTS.md` + `ai-spec-project-start` skill
- Claude Code: `CLAUDE.md`
- Cursor: `.cursor/rules/spec-driven-ai-development.mdc`
- GitHub Copilot: `.github/copilot-instructions.md`
- Generic AI tool: `AI-SESSION-INSTRUCTIONS.md`

설명은 [docs/tool-adapters.md](docs/tool-adapters.md)를 참고하세요.

예시:

```powershell
.\scripts\install-agent-adapter.ps1 -Adapter claude-code -TargetPath C:\path\to\project
```

## 핵심 규칙

Core 5:

- 현재가 과거보다 우선한다.
- 증거가 AI 자신감보다 우선한다.
- 활성 범위가 흥미로운 미래 아이디어보다 우선한다.
- 오너 결정이 AI 추진력보다 우선한다.
- 반복되는 고통은 규칙, 체크리스트, 테스트, 템플릿이 된다.
- 계획이 애매하면 저장소 증거를 먼저 확인하고, 남은 blocking 질문만
  추천 답안과 함께 묻는다.

전체 규칙은 [docs/implicit-rules.md](docs/implicit-rules.md)를 보세요.

## 주요 문서

- [docs/pattern-catalog.md](docs/pattern-catalog.md): 전체 패턴 카탈로그
- [docs/user-guide.ko.md](docs/user-guide.ko.md): 상황별 사용자 가이드와 FAQ
- [docs/anti-patterns.md](docs/anti-patterns.md): 피해야 할 실패 패턴
- [docs/fit-assessment.md](docs/fit-assessment.md): 적용 적합도 자가진단
- [docs/maintenance-cost.md](docs/maintenance-cost.md): 제어 파일 유지 비용
- [docs/operating-intensity.md](docs/operating-intensity.md): Standard/Full 운영 강도
- [docs/session-handoff.md](docs/session-handoff.md): 긴 세션 handoff와 컨텍스트 연속성
- [docs/implementation-notes.md](docs/implementation-notes.md): 명세에 없던 구현 의사결정 기록
- [docs/diagrams.md](docs/diagrams.md): Mermaid 다이어그램
- [templates/project-control-files](templates/project-control-files): 프로젝트 제어 파일 템플릿

## 검증

```bash
python scripts/validate_repo.py
```

## 라이선스

MIT. 자세한 내용은 [LICENSE](LICENSE)를 참고하세요.
