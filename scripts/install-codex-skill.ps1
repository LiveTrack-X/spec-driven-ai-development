param(
    [switch]$Force
)

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

if ((Test-Path -LiteralPath $target) -and -not $Force) {
    throw "Target exists: $target. Re-run with -Force to replace it."
}

$stage = Join-Path $targetRoot (".ai-spec-project-start.stage." + [guid]::NewGuid().ToString("N"))
$backup = $null
try {
    Copy-Item -LiteralPath $source -Destination $stage -Recurse -Force
    if (-not (Test-Path -LiteralPath (Join-Path $stage "SKILL.md") -PathType Leaf)) {
        throw "Staged skill is incomplete: $stage"
    }

    if (Test-Path -LiteralPath $target) {
        $targetItem = Get-Item -Force -LiteralPath $target
        if (($targetItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
            throw "Refusing to replace linked skill target: $target"
        }
        if (-not $targetItem.PSIsContainer) {
            throw "Skill target is not a directory: $target"
        }

        $backup = Join-Path $targetRoot (".ai-spec-project-start.backup." + [guid]::NewGuid().ToString("N"))
        [System.IO.Directory]::Move($target, $backup)
        try {
            [System.IO.Directory]::Move($stage, $target)
            $stage = $null
        } catch {
            $replacementError = $_.Exception.Message
            if (-not (Test-Path -LiteralPath $target)) {
                try {
                    [System.IO.Directory]::Move($backup, $target)
                    $backup = $null
                } catch {
                    throw "Skill replacement and rollback failed. Previous installation retained at $backup. $replacementError"
                }
                throw "Skill replacement failed; the previous installation was restored. $replacementError"
            }
            throw "Skill replacement failed because the target reappeared. Previous installation retained at $backup. $replacementError"
        }
        Remove-Item -LiteralPath $backup -Recurse -Force
        $backup = $null
    } else {
        [System.IO.Directory]::Move($stage, $target)
        $stage = $null
    }
} finally {
    if ($stage -and (Test-Path -LiteralPath $stage)) {
        Remove-Item -LiteralPath $stage -Recurse -Force
    }
}

Write-Host "Installed ai-spec-project-start skill to $target"
Write-Host "Restart Codex or start a new session, then use: `$ai-spec-project-start"
