# 사용자 가이드와 FAQ

[English](user-guide.md) | [한국어](user-guide.ko.md) | [中文](user-guide.zh.md) | [日本語](user-guide.ja.md)

이 문서는 한국어 안내용입니다. 영어 [user-guide.md](user-guide.md), `docs/`,
`templates/`, `scripts/`가 영어 기준 문서입니다. 내용이 다르면 영어 기준을 우선하세요.

SDAD Protocol(SPEC-Directed AI Development)은 AI 보조 개발을 위한 저장소 기반
운영 프로토콜입니다. 구현 방법이나 AI 도구를 정하지 않고 현재 범위, validation,
evidence, unresolved state, owner authority를 일관되게 유지합니다. AI가 맞다고
보장하거나 tests, CI, permissions, review를 대체하지 않습니다.

## 먼저 구분할 세 가지

> Scale은 어떤 제어 문서를 유지할지, `execution_scope`는 AI가 현재 어디까지 진행할지,
> owner gate는 어떤 행동에서 반드시 멈출지를 결정합니다.

| 축 | 소유하는 것 | 소유하지 않는 것 |
|---|---|---|
| Scale | 유지할 control surface | 작업 허가 범위 |
| `execution_scope` | `unit` 또는 `packet` 실행 경계 | 위험 수락 |
| owner gate | 보호 행동에 대한 권한 | 구현 품질 |
| validation contract | 검사와 증명 범위 | owner acceptance |
| handoff | 세션 간 복구 포인터 | 현재 source of truth |

## 빠른 선택

| 상황 | Scale | 기본값 |
|---|---|---|
| 현재 요청만 처리하고 지속 파일이 필요 없음 | One-shot | 현재 요청, SDAD file 없음 |
| 작은 기능이나 bug fix | Mini | `execution_scope: unit` |
| 여러 세션, review, TODO, 상태 유지가 필요 | Standard | `execution_scope: packet` |
| release, migration, security, data, production 위험 | Full | `execution_scope: packet` + 필요한 owner gates |

사용자는 평소 목표만 말하면 됩니다. AI가 repository와 요청을 근거로 먼저 추론하고,
판단할 수 없는 항목이 Scale이나 owner gate를 실질적으로 바꿀 때만 추천 답안이 있는
blocking 질문을 하나 묻습니다.

권장 해석 보고:

```text
Scale: Standard
Execution scope: packet
Reason: multi-session state and review findings already exist.
Owner gates: release only
Unresolved question: none
```

## 자연어 요청

정확한 SDAD 명령어나 skill 이름을 외울 필요가 없습니다.

| 이렇게 말하면 | AI가 해석할 intent |
|---|---|
| "전체를 보고 문제를 찾아줘" | review/audit intent |
| "현재 SPEC대로 구현해줘" | implementation intent |
| "release 전에 멈춰" | release owner gate가 있는 packet |
| "다음 세션이 이어서 하게 해줘" | handoff intent |
| "이 repo에서 채택할 만한 것을 찾아줘" | reference-intake intent |
| "승인 요청이 너무 많아" | `execution_scope` 및 owner-gate 승인·만료 조정 intent |
| "commit and wait" | commit에서 멈춤; push/release/deploy 권한은 아님 |

"carefully", "fully", "quickly" 같은 수식어는 검토 깊이나 압축 정도를 바꿀 뿐
scope를 넓히지 않습니다. `evidence-ready`도 Owner가 수락하기 전에는 최종 완료가 아닙니다.
현재 적용 가능한 Owner 지시가 이전 방향보다 우선합니다. 방향이 바뀌면 영향받은 작업을
멈추고 Plan -> Route로 돌아가 SPEC/state를 정렬합니다. 명확한 명령형은 명시한 행동과
경계만 승인합니다. 질문, 가정, 인용, 부정문, review/reference-only 요청은 그 안에 언급된
행동을 승인하지 않습니다.

## 하나의 작업 루프

1. Plan — 목표, scope, acceptance, evidence, gate를 정합니다.
2. Route — adapter, state, INDEX를 따라 필요한 문서만 선택합니다.
3. Implement — 작고 review 가능한 unit으로 변경합니다.
4. Verify — validation을 실행하고 결과 및 한계를 수집합니다.
5. Report — evidence-ready 보고를 제출합니다.

Owner Gate는 보호 행동이 있을 때만, Handoff는 세션 연속성이 필요할 때만 적용하는
조건부 checkpoint입니다. 둘을 매 packet의 의무적인 추가 단계로 만들지 않습니다.

## Context를 읽는 순서

Standard/Full에서 시작할 때는 다음 순서를 사용합니다.

```text
tool adapter -> sdad-state.yaml -> docs/INDEX.md -> current source/tests -> selected routed docs
```

`routed_docs`는 현재 packet에서 선택할 수 있는 문서 목록입니다. startup 때 전부 읽으라는
명령이 아닙니다. 현재 intent에 필요한 문서만 열고, final report에는 실제로 읽은 문서만
기록합니다. archive, 큰 log, generated report, private data는 기본 context로 넣지 않습니다.
현재 Owner가 직접 지정한 입력은 오래된 `routed_docs`에 없어도 요청 범위 안에서 확인할 수
있습니다. 채택하면 stateful implementation 전에 authority와 route를 갱신합니다.

큰 Copy-Paste/bootstrap prompt는 설치 또는 업그레이드 때 한 번만 사용합니다. 설치 후에는
그 프롬프트를 매번 다시 읽거나 붙여 넣지 말고 adapter -> state -> INDEX를 따릅니다.

도구의 native session, checkpoint, doctor 기능은 편의 또는 도구 상태 진단입니다.
SDAD의 `sdad-state.yaml`, `current_handoff`, Doctor report를 대체하지 않습니다.

## 상태와 handoff

state v2에서는 `current_handoff`가 유일한 선택적 현재 연속성 포인터입니다. 값이 있으면
해당 문서의 packet marker가 active packet과 일치해야 합니다. 긴 내용을 handoff에 복제하지
말고 SPEC, TODO, findings, ADR, evidence의 경로와 다음 행동을 연결하세요.

`save-state.md`는 v3.1 migration 때만 읽는 legacy 입력입니다. v2로 옮긴 뒤에는 두 번째
현재 상태 문서로 계속 갱신하지 않습니다. 새 handoff는 필요할 때
`docs/sdad/handoffs/YYYY-MM-DD-HNNNN-topic.md`에 만듭니다. `HNNNN`은 같은 날짜
안에서만 증가하고 새 날짜의 첫 handoff는 `H0001`로 다시 시작합니다. 다른 날짜에 같은
`HNNNN`이 있을 수 있으므로 전체 경로로 참조합니다. 기존 무번호 handoff는 유지하며
현재성은 `current_handoff`만 결정합니다.

## Owner gate 승인 재사용

조건부 승인은 다음 exact field로 기록할 수 있습니다.

```text
Decision:
Authorized action:
Packet:
Conditions:
Source/artifact identity:
Expires when:
Evidence required before action:
```

`Authorized action`, `Packet`, `Conditions`, `Source/artifact identity`,
`Evidence required before action`이 그대로이고, `Expires when`에 도달하지 않았다면 같은 승인을 다시
묻지 않습니다. 이 중 하나라도 달라지면 승인은 만료되고 Owner의 새 결정이 필요합니다.
나중의 제한, 취소, 철회는 영향받은 승인을 즉시 끝냅니다. 대체 packet 없이 취소하면
`deferred`로 기록하고 resume trigger를 명시적 Owner 재활성화로 고정하며 자동 재개하지 않습니다.

## 한 사실은 한 곳에만 기록

| 내용 | 기준 위치 |
|---|---|
| 의도한 범위, 동작, acceptance criteria | state가 선언한 `active_spec` |
| 관찰된 동작 | 현재 source, tests, runtime, 재현 가능한 명령 |
| 작은 비명세 구현 판단 | `docs/implementation-notes.md` |
| 되돌리기 어려운 구조 결정 | ADR |
| 아직 해결하지 않은 일 | TODO 또는 finding |
| Owner 승인 또는 acceptance | 하나의 권위 있는 owner-decision record |
| 다음 세션 복구 정보 | handoff |
| 현재 실행 상태 | `sdad-state.yaml` |

handoff는 위 문서의 내용을 복제하지 않고 경로와 핵심 결과만 연결합니다.
`SPEC-COMPLETE.md`의 COMPLETE는 통합 baseline이라는 뜻이지 불변의 최종본이라는
뜻이 아닙니다. stateful project에서는 `active_spec` 하나만 normative SPEC 진입점입니다.
파일의 존재, 이름, 날짜, 상태만으로 SPEC 권위가 생기지는 않습니다. Owner가 채택·반영·구현을
지시하면 현재 change request이므로 영향받은 작업을 멈추고 active boundary와 조정합니다.
검토·비교·설명·draft/reference-only 요청은 read-only이고, 단순히 발견된 SPEC도 자동 권위가
없습니다. 같은 미완료 acceptance 경계면 기존 packet을 amend할 수 있지만, 중대한 변경이나
accepted packet 뒤의 변경은 새 packet ID와 새 validation을 사용합니다.

state가 terminal packet을 떠나기 전, 하나의 durable decision record가 packet ID,
active SPEC path와 exact revision, source/artifact identity, evidence와 claim limits,
unresolved risk, final owner decision을 함께 고정해야 합니다.

owner-decision record는 결정마다 하나의 권위이며 하나의 전역 파일을 뜻하지 않습니다.
terminal 결정을 수정·제한·철회할 때는 과거 record를 고치지 말고 고유 ID가 있는 새
record에 `Revises/supersedes`를 기록한 뒤, 영향받는 current-claim pointer를 옮기세요.
같은 predecessor와 겹치는 claim scope를 수정하는 parallel decision이 생기면 affected
claim을 hold하고, owner reconciliation record가 모든 competing successor를 정리할
때까지 date나 ID로 current authority를 고르지 마세요.

장기 작업 중 SPEC, source, dependency, environment, artifact, gate, 외부 결과가 바뀌면
Plan -> Route로 재진입합니다. 같은 미완료 objective와 acceptance 경계일 때만 같은 packet을
유지합니다. 읽기 전용 review나 planning은 Implement를 생략할 수 있지만 보고서에 N/A 또는
blocked 이유를 쓰고, 생략한 단계의 evidence를 주장하면 안 됩니다.

## Evidence와 주장 한계

| 증거 | 말할 수 있는 것 | 말할 수 없는 것 |
|---|---|---|
| Doctor green | 선언된 구조가 일관됨 | 기능 정확성, 효과, Owner 수락 |
| task benchmark 성공 | 특정 task를 성공함 | 전체적으로 이전보다 나음 |
| controlled comparison 성공 | 비교 조건에서 개선됨 | 다른 조건에도 자동 적용됨 |

AI가 done이라고만 말하면 changed files, checks, docs checked, limits,
partial/degraded/unverified behavior, open findings, 필요한 Owner decision을 포함한
`evidence-ready` 보고를 요구하세요. `owner-accepted`는 별도 상태입니다.

## 문제 해결 FAQ

### AI가 repository를 보기 전에 질문합니다

먼저 code, tests, active docs, SPEC, TODO, findings, ADR을 확인하게 하세요. 그 뒤에도
Scale이나 gate를 바꾸는 불확실성이 있으면 추천 답안이 있는 질문 하나만 허용합니다.

### 승인 요청이 너무 잦거나 AI가 너무 멀리 갑니다

`execution_scope`가 `unit | packet` 중 무엇인지 확인하세요. 작은 micro-task를 묶어 처리하려면
`packet`을 사용합니다. 여러 packet을 연속 실행하려면 Owner가 packet 목록이 있는 계획을
명시적으로 승인해야 합니다. 시간 단위인 session은 실행 범위 값이 아닙니다.

### SDAD 파일이 너무 많습니다

지속성이 없으면 One-shot, 작은 작업이면 Mini를 선택하세요. Standard/Full에서도
`routed_docs`를 전부 읽지 말고 현재 intent에 필요한 것만 선택합니다.

### formal test가 없습니다

가능한 가장 강한 practical evidence를 사용하고 한계를 밝히세요. build/lint/typecheck,
targeted script, smoke test, API response, log, screenshot, manual reproduction, docs diff가
될 수 있습니다.

### chat-only tool이 설치했다고 말합니다

project filesystem을 편집하지 못하면 설치된 것이 아닙니다. Claude.ai나 ChatGPT web에서는
planning만 하고 실제 adapter 설치는 coding tool에서 수행합니다.

## 다음에 읽을 문서

- [getting-started.md](getting-started.md): 설치와 첫 실행
- [no-clone-quick-install.md](no-clone-quick-install.md): clone 없는 one-time bootstrap
- [mini-sdad.md](mini-sdad.md): 작은 프로젝트
- [owners-guide.md](owners-guide.md): Owner 운영
- [ai-work-loop.md](ai-work-loop.md): 실행 루프
- [session-handoff.md](session-handoff.md): handoff 계약
- [implementation-notes.md](implementation-notes.md): 구현 판단 기록

## v3.1 용어를 사용하던 경우

이 절은 migration/history 전용입니다. Level 0 Ask-first는 미승인 상태, Level 1 Unit Autonomy는
`unit`, Level 2 Work Packet Autonomy는 `packet`으로 해석할 수 있습니다. Level 3 Session
Autonomy는 session을 scope로 옮기지 말고 승인된 packet 목록으로 표현합니다. Level 4
Release-gated Autonomy는 execution scope가 아니라 owner gates로 옮깁니다. Q5는 강제 질문이
아니며 operating intensity도 state v2 field가 아닙니다. 자세한 과거 매핑은
[autonomy-levels.md](autonomy-levels.md), [operating-intensity.md](operating-intensity.md)를
참고하되 새 state에는 legacy 용어를 기록하지 마세요.

기존 evidence/claim 표의 owner-acceptance 행은 이력으로 보존하세요. 각 결정을 다음에
수정할 때 하나의 durable decision record를 선택하고, 나머지 변경 가능한 acceptance field는
그 기록을 가리키는 link로 바꾸면 됩니다. 일괄 재작성은 필요하지 않습니다.
