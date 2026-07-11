# SDAD Protocol

[English](README.md) | [한국어](README.ko.md) | [中文](README.zh.md) | [日本語](README.ja.md)

상태: `3.1.0` 안정 문서/패키지 릴리즈.

효과는 프로젝트 적합도, 오너의 운영 규율, evidence 품질에 따라 달라집니다.

이 문서는 한국어 안내용 README입니다. 영어 [README.md](README.md)와 영어 기반
`docs/`, `templates/`, `scripts/`가 기준입니다. 내용이 다르면 영어 기준 문서를
우선하세요.

## 무엇인가

SDAD Protocol(SPEC-Driven AI Development)은 여러 AI 도구와 세션이 저장소에서
일할 때 상태, 범위, 증거, 오너 권한, 의사결정, handoff가 서로 어긋나지 않게 하는
저장소 로컬 작업 규약입니다. Markdown은 권한과 기대를 기록하지만 도구 사용을
기술적으로 차단하지는 않습니다. 실제 강제는 permissions, hooks, sandbox,
branch protection 같은 실행 환경이 담당합니다.

핵심 원칙은 간단합니다.

- Scale은 유지할 제어 표면을 정합니다.
- `execution_scope`는 AI가 지금 어디까지 실행할 수 있는지 정합니다.
- owner gate는 어떤 보호 행동에서 반드시 멈춰야 하는지 정합니다.
- validation contract는 어떤 검사가 무엇을 증명하고 무엇을 증명하지 않는지 정합니다.
- `evidence-ready`는 검토 가능한 AI 결과이고, `owner-accepted`는 오너의 최종 수락입니다.

## 빠른 선택

AI가 저장소와 요청을 먼저 검사해 가장 작은 안전한 Scale, `execution_scope`,
owner gate를 추론합니다. 이 판단이 실질적으로 달라지는 불확실성이 남을 때만
추천 답안과 함께 한 가지 질문을 합니다. 사용자는 언제든 추론 결과를 덮어쓸 수 있습니다.

| Scale | 기본 실행 경계 | 기본 제어 |
|---|---|---|
| One-shot | 현재 요청 | 영구 SDAD 파일 없음 |
| Mini | `unit` | 작은 작업을 위한 최소 instruction과 evidence |
| Standard | `packet` | 지속 상태, SPEC, TODO, review, validation |
| Full | `packet` | Standard + release/security/data 등 이름이 명시된 owner gates |

Scale과 위험 권한은 별개입니다. 작은 작업도 위험 행동에는 gate가 필요하고,
Full이라고 해서 보호 행동이 자동 승인되지는 않습니다.

## 하나의 작업 루프

모든 Scale은 하나의 5단계 루프를 사용합니다.

1. Plan — 목표, 범위, acceptance, 증거를 정합니다.
2. Route — state와 `docs/INDEX.md`에서 지금 필요한 정보만 고릅니다.
3. Implement — 작고 리뷰 가능한 단위로 변경합니다.
4. Verify — validation을 실행하고 결과와 한계를 수집합니다.
5. Report — evidence-ready 결과, 위험, 미검증 항목을 보고합니다.

Owner Gate와 Handoff는 항상 추가되는 단계가 아니라 조건부 checkpoint입니다.
보호 행동이 있으면 gate에서 멈추고, 다음 세션으로 넘겨야 할 때만 handoff를 만듭니다.

## 컨텍스트와 연속성

Standard/Full 시작 경로는 tool adapter -> `sdad-state.yaml` -> `docs/INDEX.md`입니다.
`routed_docs`는 시작할 때 전부 읽는 목록이 아니라 현재 packet에서 선택할 수 있는
문서 집합입니다. 에이전트는 현재 intent에 필요한 문서만 읽고 실제로 읽은 경로를
보고해야 합니다.

state v2에서는 `current_handoff`가 유일한 선택적 현재 연속성 포인터입니다.
`save-state.md`는 v3.1 프로젝트를 옮길 때만 사용하는 legacy migration 입력이며,
현재 상태의 두 번째 source of truth가 아닙니다.

큰 Copy-Paste/bootstrap 프롬프트는 설치 또는 업그레이드 때 한 번만 사용합니다.
설치 후의 일반 작업에서는 그 프롬프트를 매 세션 다시 붙여 넣지 말고 adapter,
state, INDEX를 따릅니다. 도구 자체의 session/checkpoint/doctor 기능은 편의 기능 또는
도구 진단일 뿐 SDAD state, handoff, Doctor의 권위를 대신하지 않습니다.

## Owner gate와 사전 승인

같은 승인을 반복해서 묻지 않도록 조건부 사전 승인을 기록할 수 있습니다.

```text
Decision:
Authorized action:
Packet:
Conditions:
Expires when:
Evidence required before action:
```

승인은 `Authorized action`, `Packet`, `Conditions`, `Evidence required before action`이
그대로이고, 승인 후 source가 변경되지 않았으며, `Expires when`에 도달하지 않은 동안만
재사용합니다. 이 중 하나라도 달라지면 다시 오너 결정을 받아야 합니다.

## Evidence와 완료 주장

- Doctor green: 구조와 선언의 일관성만 확인합니다.
- task benchmark 성공: 지정한 작업을 성공했다는 증거입니다.
- controlled comparison 성공: 이전 방식보다 실제로 낫다는 주장에 필요한 증거입니다.

Doctor나 unit test만으로 생산성 향상, 정확성, 오너 수락을 주장하지 않습니다.
AI는 변경 파일, 실행한 검사, 문서 확인, 한계, 미검증 항목, 열린 finding을 포함한
`evidence-ready` 보고를 제출합니다. 최종 완료는 오너가 `owner-accepted`로 수락해야 합니다.

## 빠른 시작

처음에는 [docs/getting-started.md](docs/getting-started.md)를 읽으세요. 저장소를
클론하지 않고 시작하려면 [docs/no-clone-quick-install.md](docs/no-clone-quick-install.md),
작은 프로젝트라면 [docs/mini-sdad.md](docs/mini-sdad.md)를 사용하세요.

자세한 한국어 설명과 문제 해결은 [docs/user-guide.ko.md](docs/user-guide.ko.md),
적합도는 [docs/fit-assessment.md](docs/fit-assessment.md), 유지 비용은
[docs/maintenance-cost.md](docs/maintenance-cost.md)를 참고하세요.

도구별 adapter:

- Codex: `AGENTS.md` + `ai-spec-project-start` skill
- Claude Code: `CLAUDE.md`
- Cursor: `.cursor/rules/spec-driven-ai-development.mdc`
- GitHub Copilot: `.github/copilot-instructions.md`
- Generic AI tool: `AI-SESSION-INSTRUCTIONS.md`

Claude.ai나 ChatGPT web처럼 project filesystem을 편집할 수 없는 chat-only 환경에서는
계획만 할 수 있으며 adapter를 설치했다고 주장하면 안 됩니다.

## 문제 해결 FAQ

- 정확한 SDAD 명령어나 skill 이름을 모르면 자연어로 요청하세요. AI는 interpreted intent,
  Scale, `execution_scope`, evidence, owner gate를 짧게 밝힙니다.
- 승인 요청이 잦으면 `execution_scope: packet`인지 확인하세요. release 같은 보호 행동은
  별도의 gate로 남습니다.
- AI가 done이라고만 하면 `evidence-ready` 보고와 오너 수락 상태를 구분하게 하세요.
- 다음 세션이 맥락을 잃으면 `current_handoff`와 packet marker가 일치하는지 확인하세요.
- blocking 질문은 저장소 증거를 먼저 검사한 뒤 결정에 필요한 한 가지로 제한하세요.
- 한 packet 안에서는 리뷰 의미가 있는 개발 단위를 이어서 처리하고 증거와 함께 멈춥니다.

## 주요 문서

- [docs/owners-guide.md](docs/owners-guide.md): 오너용 빠른 도입 가이드
- [docs/ai-work-loop.md](docs/ai-work-loop.md): 단일 실행 루프
- [docs/session-handoff.md](docs/session-handoff.md): 조건부 handoff와 연속성
- [docs/implementation-notes.md](docs/implementation-notes.md): 명세 밖 구현 판단
- [docs/pattern-catalog.md](docs/pattern-catalog.md): 패턴 카탈로그

## 검증

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
git diff --check
```

## v3.1에서 마이그레이션하는 경우

v3.1의 Level 0 Ask-first, Level 1 Unit Autonomy, Level 2 Work Packet Autonomy,
Level 3 Session Autonomy, Level 4 Release-gated Autonomy는 새 상태 필드가 아닙니다.
실행 경계는 `unit | packet`, 보호 권한은 owner gates로 분리하세요. Q5는 질문 의식이
아니라 위험을 추론하는 과거 표현입니다. operating intensity도 state v2에서 제거됐습니다.
기존 `save-state.md`, [docs/operating-intensity.md](docs/operating-intensity.md),
[docs/autonomy-levels.md](docs/autonomy-levels.md)는 migration/history 참고용입니다.
Full SDAD / High, 고급 확장 같은 표현은 새 프로젝트의 실행 계약으로 복사하지 마세요.

## 라이선스

MIT. 자세한 내용은 [LICENSE](LICENSE)를 참고하세요.
