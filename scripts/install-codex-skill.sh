#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 [--force]" >&2
}

force="${1:-}"
if [[ $# -gt 1 || ( -n "${force}" && "${force}" != "--force" ) ]]; then
  usage
  exit 1
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
source_dir="${repo_root}/skills/ai-spec-project-start"
target_root="${CODEX_HOME:-${HOME}/.codex}/skills"

if [[ ! -d "${source_dir}" ]]; then
  echo "Skill source not found: ${source_dir}" >&2
  exit 1
fi

mkdir -p "${target_root}"
target_root="$(cd "${target_root}" && pwd -P)"
target_dir="${target_root}/ai-spec-project-start"

case "${target_dir}" in
  "${target_root}/"*) ;;
  *)
    echo "Refusing to install outside the Codex skills directory: ${target_dir}" >&2
    exit 1
    ;;
esac

if [[ -L "${target_dir}" ]]; then
  echo "Refusing to replace linked skill target: ${target_dir}" >&2
  exit 1
fi
if [[ -e "${target_dir}" && ! -d "${target_dir}" ]]; then
  echo "Skill target is not a directory: ${target_dir}" >&2
  exit 1
fi

if [[ -e "${target_dir}" && "${force}" != "--force" ]]; then
  echo "Target exists: ${target_dir}. Re-run with --force to replace it." >&2
  exit 1
fi

stage_dir="$(mktemp -d "${target_root}/.ai-spec-project-start.stage.XXXXXX")"
backup_dir=""
move_directory_exact() {
  local source_path="$1"
  local destination_path="$2"
  local nested_path

  if mv --help 2>&1 | grep -q -- '--no-target-directory'; then
    mv -T -n -- "${source_path}" "${destination_path}"
    if [[ -e "${source_path}" || -L "${source_path}" ]]; then
      return 1
    fi
    return 0
  fi

  if ! mv -n -- "${source_path}" "${destination_path}"; then
    return 1
  fi
  if [[ -e "${source_path}" || -L "${source_path}" ]]; then
    return 1
  fi
  nested_path="${destination_path}/$(basename "${source_path}")"
  if [[ -e "${nested_path}" || -L "${nested_path}" ]]; then
    if mv -- "${nested_path}" "${source_path}"; then
      return 1
    fi
    echo "Exact move failed; transaction data retained at ${nested_path}." >&2
    return 2
  fi
  return 0
}

cleanup() {
  if [[ -n "${stage_dir}" && ( -e "${stage_dir}" || -L "${stage_dir}" ) ]]; then
    rm -rf -- "${stage_dir}"
  fi
}
trap cleanup EXIT

cp -R "${source_dir}/." "${stage_dir}/"
if [[ ! -f "${stage_dir}/SKILL.md" ]]; then
  echo "Staged skill is incomplete: ${stage_dir}" >&2
  exit 1
fi

if [[ -e "${target_dir}" ]]; then
  backup_dir="$(mktemp -d "${target_root}/.ai-spec-project-start.backup.XXXXXX")"
  rmdir -- "${backup_dir}"
  move_directory_exact "${target_dir}" "${backup_dir}"
  if ! move_directory_exact "${stage_dir}" "${target_dir}"; then
    if move_directory_exact "${backup_dir}" "${target_dir}"; then
      echo "Skill replacement failed; the previous installation was restored." >&2
    else
      echo "Skill replacement and rollback failed. Previous installation retained at ${backup_dir}." >&2
    fi
    exit 1
  fi
  stage_dir=""
  rm -rf -- "${backup_dir}"
else
  if ! move_directory_exact "${stage_dir}" "${target_dir}"; then
    echo "Skill installation failed because the exact target path was not available." >&2
    exit 1
  fi
  stage_dir=""
fi

trap - EXIT

echo "Installed ai-spec-project-start skill to ${target_dir}"
echo 'Restart Codex or start a new session, then use: $ai-spec-project-start'
