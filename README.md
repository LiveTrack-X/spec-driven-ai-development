# SPEC-Driven AI Development

Owner-supervised, multi-agent, evidence-based software development with AI agents and living SPECs.

This repository packages a reusable workflow for people who use AI agents to plan, specify, implement, review, and maintain software while keeping a human owner in control of direction, risk, and completion decisions.

The workflow is field-derived from two project styles:

- CMP-style project control: documentation routing, source-of-truth order, active TODO/review ledgers, and production-readiness hardening.
- DirectPipe-style release control: version lanes, migration maps, risk-domain rules, release gates, and cross-AI pre-release review.

## Korean Summary

이 저장소는 AI 에이전트를 단순 코딩 도구가 아니라 기획자, SPEC 작성자, 구현자, 리뷰어, QA 파트너로 나누어 쓰기 위한 프로젝트 운영 템플릿입니다.

핵심은 다음입니다.

- 인간 오너가 방향과 완료 판단을 가진다.
- AI는 기획, SPEC, 구현, 리뷰, 검증을 돕는다.
- SPEC은 작업 기준이지만, 완료 증거는 코드, 테스트, 문서, 재현 가능한 결과다.
- 다른 AI, 모델, 세션으로 교차 검토한다.
- 이전 프로젝트의 불편함은 다음 프로젝트의 운영 규칙으로 바꾼다.

## What This Is

This is not just "AI writes code from a spec."

It is a project-control loop:

```text
prior pain / product need
-> owner + AI planning
-> active SPEC
-> bounded implementation
-> cross-model review
-> tests and docs evidence
-> owner decision
-> operating rule or backlog update
```

The owner may not write code directly. The workflow is designed so the owner can still govern development through clear SPECs, small implementation slices, review findings, tests, documentation checks, and explicit acceptance decisions.

## Why This Exists

AI-assisted projects often fail in the same ways:

- every session starts from a different context,
- docs multiply until nobody knows what is current,
- AI claims completion without enough evidence,
- old plans override current code,
- reviewers find issues that never enter a durable backlog,
- non-coders cannot reliably supervise implementation progress.

This workflow turns those problems into a project control system.

## What's Included

```text
prompts/
  kickoff-prompt.md
  review-prompt.md
  handoff-prompt.md
docs/
  pattern-catalog.md
  field-notes/
skills/
  ai-spec-project-start/
templates/
  project-control-files/
examples/
  minimal-project/
scripts/
  install-codex-skill.ps1
  install-codex-skill.sh
  validate_repo.py
```

## Quick Start

Use the kickoff prompt in any capable AI coding environment:

```text
Use the SPEC-driven AI development workflow from this repository.
Start by clarifying the product pain, owner control model, active SPEC, non-goals, risks, and evidence required for completion.
```

Or open [prompts/kickoff-prompt.md](prompts/kickoff-prompt.md) and paste it into your AI session.

For the full method, read [docs/pattern-catalog.md](docs/pattern-catalog.md). For the field notes behind the method, read [docs/field-notes/cmp-development-method.md](docs/field-notes/cmp-development-method.md) and [docs/field-notes/directpipe-development-method.md](docs/field-notes/directpipe-development-method.md).

## Install The Codex Skill

Windows PowerShell:

```powershell
.\scripts\install-codex-skill.ps1
```

macOS/Linux:

```bash
./scripts/install-codex-skill.sh
```

Then start a new Codex session and say:

```text
$ai-spec-project-start 사용해서 새 프로젝트 시작 구조 잡아줘.
```

If your session does not auto-discover newly installed skills yet, reference the skill path directly:

```text
Use the skill at ~/.codex/skills/ai-spec-project-start to bootstrap this project.
```

## Use The Project Templates

Copy the files under [templates/project-control-files](templates/project-control-files) into a new project, then adapt them:

- `AGENTS.md`: mandatory AI agent start rules.
- `docs/INDEX.md`: single documentation routing table.
- `docs/Repository-Operating-Rules.md`: durable rulebook for repeated agent rules.
- `SPEC/SPEC-COMPLETE.md`: canonical current product and implementation baseline.
- `docs/TODO-Open-Items.md`: current open implementation work.
- `review-findings.md`: active bugs and review findings.
- `README.md`: human-facing project summary.

## Field-Proven Controls

Use CMP-style controls when the problem is context drift, scattered docs, unclear completion status, or production-readiness uncertainty.

Use DirectPipe-style controls when the problem is stable-vs-next version management, migration risk, release packaging, platform differences, or fragile runtime behavior.

Most serious AI-assisted projects need both: CMP keeps the project intelligible across sessions, while DirectPipe-style gates keep risky releases and refactors honest.

## Source Of Truth

When sources conflict, prefer:

1. Source code, migrations, tests, reproducible commands
2. Active runtime docs
3. Canonical SPEC
4. Active SPEC files
5. Handoff/save-state files
6. Product notes and external references
7. Historical or archived records
8. Chat memory or AI confidence

## AI Role Split

- Planning AI: turns owner pain into product scope and non-goals.
- SPEC AI: writes implementation-ready SPEC with acceptance criteria.
- Builder AI: implements a bounded slice.
- Reviewer AI: finds bugs, security risks, missing tests, docs drift, and overreach.
- QA AI: tries to reproduce behavior and verify commands.
- Maintainer AI: updates docs, TODO, findings, and handoff.
- Owner: sets direction, priority, risk tolerance, and final acceptance.

## Validate This Repository

```bash
python scripts/validate_repo.py
```

## License

MIT. See [LICENSE](LICENSE).
