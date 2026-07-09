#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <codex|claude-code|cursor|github-copilot|generic> [target-path] [--force]" >&2
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

adapter="$1"
target_root="${2:-.}"
force="${3:-}"

if [[ "${force}" != "" && "${force}" != "--force" ]]; then
  usage
  exit 1
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
target_root="$(cd "${target_root}" && pwd)"

case "${adapter}" in
  codex)
    source_rel="adapters/codex/AGENTS.md"
    target_rel="AGENTS.md"
    ;;
  claude-code)
    source_rel="adapters/claude-code/CLAUDE.md"
    target_rel="CLAUDE.md"
    ;;
  cursor)
    source_rel="adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc"
    target_rel=".cursor/rules/spec-driven-ai-development.mdc"
    ;;
  github-copilot)
    source_rel="adapters/github-copilot/.github/copilot-instructions.md"
    target_rel=".github/copilot-instructions.md"
    ;;
  generic)
    source_rel="adapters/generic/AI-SESSION-INSTRUCTIONS.md"
    target_rel="AI-SESSION-INSTRUCTIONS.md"
    ;;
  *)
    usage
    exit 1
    ;;
esac

source_path="${repo_root}/${source_rel}"
target_path="${target_root}/${target_rel}"

if [[ ! -f "${source_path}" ]]; then
  echo "Adapter source not found: ${source_path}" >&2
  exit 1
fi

if [[ -e "${target_path}" && "${force}" != "--force" ]]; then
  echo "Target exists: ${target_path}. Re-run with --force to overwrite." >&2
  exit 1
fi

mkdir -p "$(dirname "${target_path}")"
cp "${source_path}" "${target_path}"

echo "Installed ${adapter} adapter file: ${target_path}"
echo "Done. Review the installed file and adapt project-specific paths if needed."
