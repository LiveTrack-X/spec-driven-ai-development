#!/usr/bin/env bash
set -euo pipefail

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

rm -rf "${target_dir}"
cp -R "${source_dir}" "${target_dir}"

echo "Installed ai-spec-project-start skill to ${target_dir}"
echo 'Restart Codex or start a new session, then use: $ai-spec-project-start'
