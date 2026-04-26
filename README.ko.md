# SPEC-Driven AI Development

[English](README.md) | [한국어](README.ko.md) | [中文](README.zh.md) | [日本語](README.ja.md)

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
`save-state.md`를 사용하는 프로젝트라면 세션 종료/중단, handoff, 오너 방향 변경,
부분/미검증 상태, 또는 다음 세션이 컨텍스트를 다시 구성하기 어려운 경우에도 최신화해야 합니다.
Mini SDAD도 완료 기준이 있습니다. 변경 파일, 확인 증거, 한계/미검증 항목,
오너 수락이 보이기 전에는 done으로 보지 않습니다.
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

전체 규칙은 [docs/implicit-rules.md](docs/implicit-rules.md)를 보세요.

## 주요 문서

- [docs/pattern-catalog.md](docs/pattern-catalog.md): 전체 패턴 카탈로그
- [docs/anti-patterns.md](docs/anti-patterns.md): 피해야 할 실패 패턴
- [docs/fit-assessment.md](docs/fit-assessment.md): 적용 적합도 자가진단
- [docs/diagrams.md](docs/diagrams.md): Mermaid 다이어그램
- [templates/project-control-files](templates/project-control-files): 프로젝트 제어 파일 템플릿

## 검증

```bash
python scripts/validate_repo.py
```

## 라이선스

MIT. 자세한 내용은 [LICENSE](LICENSE)를 참고하세요.
