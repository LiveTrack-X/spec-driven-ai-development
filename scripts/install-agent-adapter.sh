#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <codex|claude-code|gemini-cli|cursor|github-copilot|generic> [target-path] [--force]" >&2
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

adapter="$1"
shift
target_root="."
force=""

if [[ $# -gt 0 && "$1" != "--force" ]]; then
  target_root="$1"
  shift
fi
if [[ $# -gt 0 && "$1" == "--force" ]]; then
  force="$1"
  shift
fi
if [[ $# -ne 0 ]]; then
  usage
  exit 1
fi

script_dir="$(cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
repo_root="$(cd -- "${script_dir}/.." && pwd -P)"
target_root="$(cd -- "${target_root}" && pwd -P)"

case "${adapter}" in
  codex)
    source_rel="adapters/codex/AGENTS.md"
    target_rel="AGENTS.md"
    ;;
  claude-code)
    source_rel="adapters/claude-code/CLAUDE.md"
    target_rel="CLAUDE.md"
    ;;
  gemini-cli)
    source_rel="adapters/gemini-cli/GEMINI.md"
    target_rel="GEMINI.md"
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

if [[ ! -f "${source_path}" ]]; then
  echo "Adapter source not found: ${source_path}" >&2
  exit 1
fi

target_parent_rel="$(dirname "${target_rel}")"
current_parent="${target_root}"
if [[ "${target_parent_rel}" != "." ]]; then
  IFS='/' read -r -a parent_parts <<< "${target_parent_rel}"
  for part in "${parent_parts[@]}"; do
    next_parent="${current_parent}/${part}"
    if [[ -L "${next_parent}" ]]; then
      echo "Refusing to install through linked path: ${next_parent}" >&2
      exit 1
    fi
    if [[ -e "${next_parent}" && ! -d "${next_parent}" ]]; then
      echo "Adapter target parent is not a directory: ${next_parent}" >&2
      exit 1
    fi
    if [[ ! -e "${next_parent}" ]]; then
      mkdir -- "${next_parent}"
    fi
    current_parent="${next_parent}"
  done
fi

target_path="${current_parent}/$(basename "${target_rel}")"
if [[ -L "${target_path}" ]]; then
  echo "Refusing to install through linked path: ${target_path}" >&2
  exit 1
fi
if [[ -d "${target_path}" ]]; then
  echo "Adapter target is a directory, not a file: ${target_path}" >&2
  exit 1
fi

if [[ -e "${target_path}" && "${force}" != "--force" ]]; then
  echo "Target exists: ${target_path}. Re-run with --force to overwrite." >&2
  exit 1
fi

stage_dir="$(mktemp -d "${current_parent}/.sdad-adapter.stage.XXXXXX")"
stage_path="${stage_dir}/$(basename "${target_rel}")"
cleanup() {
  rm -rf -- "${stage_dir}"
}
trap cleanup EXIT

cp -- "${source_path}" "${stage_path}"
if [[ "${force}" == "--force" ]]; then
  mv -f -- "${stage_path}" "${target_path}"
else
  if ! ln -- "${stage_path}" "${target_path}"; then
    echo "Target appeared during installation: ${target_path}. Nothing was overwritten." >&2
    exit 1
  fi
fi

if [[ ! -f "${target_path}" ]] || ! cmp -s -- "${source_path}" "${target_path}"; then
  nested_stage="${target_path}/$(basename "${stage_path}")"
  if [[ -f "${nested_stage}" ]] && cmp -s -- "${source_path}" "${nested_stage}"; then
    rm -- "${nested_stage}"
  fi
  echo "Adapter publication did not create the exact target file: ${target_path}" >&2
  exit 1
fi
if [[ -e "${stage_path}" ]]; then
  rm -- "${stage_path}"
fi
rmdir -- "${stage_dir}"
trap - EXIT

echo "Installed ${adapter} adapter file: ${target_path}"
echo "Done. Review the installed file and adapt project-specific paths if needed."
