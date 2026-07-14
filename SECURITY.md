# Security Policy

SDAD Protocol (SPEC-Directed AI Development) is a documentation, template,
adapter, and installer package. It does not ship an application runtime, but it
does publish instructions that AI coding tools may copy into other projects. Treat install
paths, raw fetch URLs, adapter content, and security-boundary wording as
security-sensitive surfaces.

## Supported Versions

Security fixes apply to the current `main` branch and the latest stable release.
For repeatable installs, use the documented full 40-character commit SHA and
SHA-256 values instead of `main`, then record the revision in your project
handoff or setup notes. A tag name alone is not an integrity boundary unless
repository policy makes it immutable.

## What To Report

Please report security issues such as:

- installer behavior that can overwrite files unexpectedly or write outside the
  requested target project,
- adapter or prompt guidance that could cause unsafe handling of secrets,
  credentials, money, auth, production data, destructive actions, releases, or
  deployments,
- supply-chain concerns in copy-paste install instructions, raw fetch URLs, or
  release artifacts,
- documentation that presents guidance as an enforced guarantee for a security
  boundary,
- validation gaps that allow security-critical instructions to drift silently.

Do not include real credentials, private data, exploit payloads, or customer
material in a public report.

## Reporting Path

Use GitHub private vulnerability reporting for this repository if it is
available. If a private channel is not available, contact the maintainer through
their GitHub profile or open a minimal public issue only to request a private
security channel. Do not publish exploit details in a public issue.

Include:

- affected file or release tag,
- expected safe behavior,
- observed unsafe behavior,
- minimal reproduction steps that do not include secrets,
- whether the issue affects `main`, a release tag, or downstream projects that
  installed an adapter.

## Boundary

This project can make security rules visible and can validate repository
structure. It cannot enforce security policy inside every downstream project.
For secrets, destructive actions, migrations, production deploys, releases,
money, auth, data, or other security boundaries, move the rule into enforced
surfaces such as CI, required tests, hooks, permissions, deny rules, branch
protection, release gates, or deployment controls.
