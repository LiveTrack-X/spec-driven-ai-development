$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$source = Join-Path $repoRoot "skills\ai-spec-project-start"
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
$targetRoot = [System.IO.Path]::GetFullPath((Join-Path $codexHome "skills"))
$target = [System.IO.Path]::GetFullPath((Join-Path $targetRoot "ai-spec-project-start"))
$rootWithSeparator = $targetRoot.TrimEnd([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar

if (-not (Test-Path -LiteralPath $source)) {
    throw "Skill source not found: $source"
}

if (-not $target.StartsWith($rootWithSeparator, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing to install outside the Codex skills directory: $target"
}

New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null

if (Test-Path -LiteralPath $target) {
    Remove-Item -LiteralPath $target -Recurse -Force
}

Copy-Item -LiteralPath $source -Destination $target -Recurse

Write-Host "Installed ai-spec-project-start skill to $target"
Write-Host "Restart Codex or start a new session, then use: `$ai-spec-project-start"
