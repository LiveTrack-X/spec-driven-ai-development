$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$source = Join-Path $repoRoot "skills\ai-spec-project-start"
$targetRoot = Join-Path $HOME ".codex\skills"
$target = Join-Path $targetRoot "ai-spec-project-start"

if (-not (Test-Path -LiteralPath $source)) {
    throw "Skill source not found: $source"
}

New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null

if (Test-Path -LiteralPath $target) {
    Remove-Item -LiteralPath $target -Recurse -Force
}

Copy-Item -LiteralPath $source -Destination $target -Recurse

Write-Host "Installed ai-spec-project-start skill to $target"
Write-Host "Restart Codex or start a new session, then use: `$ai-spec-project-start"
