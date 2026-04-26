# DirectPipe Development Method Field Note

Status: Active reference
Scope: Reusable operating patterns extracted from the DirectPipe project

This note extracts the development method, not source code. DirectPipe is useful
as a field example because it shows how AI-assisted development can govern a
real product with version lanes, cross-platform migration, real-time safety,
release gates, and high-risk implementation rules.

## What DirectPipe Teaches

### 1. Use Version Lanes

DirectPipe separates project lines by role:

- v3 stable: maintenance and critical fixes.
- v4 current/next: architecture refactor, cross-platform work, new features.

The workspace-level guide tells agents which directory and rule file apply to
each lane.

Reusable rule: when a project has stable and next-generation versions, define
allowed changes per lane before implementation begins.

### 2. Sync Critical Fixes Across Lanes

DirectPipe has a mandatory rule: a bug fixed in the stable line must be checked
and, when relevant, ported to the next line. It also warns that direct copying
can be wrong because architecture changed between lanes.

Reusable rule: bugfix sync needs a mapping table, not blind copy-paste.

### 3. Protect Existing Users During Migration

DirectPipe's migration strategy explicitly protects existing stable users from
accidental next-version updates. Release channel rules, asset naming, updater
filters, prerelease gates, and rollback thinking are part of the development
method.

Reusable rule: migrations are not just code. They need user impact analysis,
release-channel controls, compatibility rules, rollback plans, and clear
go/no-go gates.

### 4. Turn Architecture Debt Into A Named Refactor

DirectPipe records the v3 to v4 change as a mapped architecture migration:

- large UI/controller object split into focused modules,
- platform abstraction introduced,
- structured error handling introduced,
- tests expanded,
- old-to-new file mappings documented.

Reusable rule: large refactors need a visible map from old responsibilities to
new modules so future agents can port fixes and review behavior.

### 5. Make Risk Domains Explicit

DirectPipe documents thread ownership, lock hierarchy, lifetime guards,
real-time audio restrictions, platform boundaries, and DANGER ZONES. These are
not optional comments. They are operating constraints for future changes.

Reusable rule: if a project has high-risk domains, define them as first-class
rules in the agent start file and module docs.

### 6. Treat Real-Time And Lifetime Safety As Release Blockers

DirectPipe's real-time path forbids allocations, mutexes, and logging in audio
callbacks. Async UI handoffs require lifetime guards. Lock ordering violations
and cross-thread non-atomic access are documented bug classes.

Reusable rule: for fragile systems, review prompts must name the exact failure
classes to search for.

### 7. Use Multi-Layer Release Gates

DirectPipe's release checklist combines:

- automated pre-release script,
- unit and integration tests,
- dashboard API checks,
- manual checks,
- AI pre-release review,
- Critical 0 requirement.

Reusable rule: release readiness should be a gate table. "All tests passed" is
not enough when manual, platform, hardware, or reviewer evidence is required.

### 8. Admit Hardware And Platform Reality

DirectPipe separates what AI can verify from what requires real hardware or
platform access. That prevents false confidence in cross-platform work.

Reusable rule: every project should name what AI can verify, what automation can
verify, and what the owner or external tester must verify manually.

### 9. Tie Documentation Updates To Code Changes

DirectPipe requires documentation updates for new files, renamed files, thread
model changes, platform additions, new actions, and danger-zone changes.

Reusable rule: documentation rules should be triggered by change type, not by
whether the agent remembers to update docs.

## Reusable DirectPipe Rule Pack

Add these rules to projects with releases, migrations, platform work, or fragile
runtime behavior:

- Define version lanes and allowed changes per lane.
- Maintain a stable-to-next bugfix sync rule.
- Keep an architecture responsibility map for refactors.
- Document risk domains such as thread ownership, locks, security boundaries,
  data migration, external APIs, or real-time paths.
- Add release gates that combine automated tests, manual checks, AI review, and
  explicit severity thresholds.
- Document what cannot be verified by the current AI environment.
- Require rollback or recovery evidence before production/stable release claims.

## When To Use This Pattern

Use the DirectPipe-style controls when:

- the project has stable and next versions,
- a rewrite or migration is underway,
- release packaging can affect existing users,
- platform differences matter,
- runtime safety bugs are expensive,
- manual or hardware validation is unavoidable.
