param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("codex", "claude-code", "gemini-cli", "cursor", "github-copilot", "generic")]
    [string]$Adapter,

    [Parameter(Mandatory = $false)]
    [string]$TargetPath = ".",

    [switch]$Force
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$targetRoot = (Resolve-Path -LiteralPath $TargetPath).Path

$copies = @{
    "codex" = @(
        @{ Source = "adapters\codex\AGENTS.md"; Target = "AGENTS.md" }
    )
    "claude-code" = @(
        @{ Source = "adapters\claude-code\CLAUDE.md"; Target = "CLAUDE.md" }
    )
    "gemini-cli" = @(
        @{ Source = "adapters\gemini-cli\GEMINI.md"; Target = "GEMINI.md" }
    )
    "cursor" = @(
        @{ Source = "adapters\cursor\.cursor\rules\spec-driven-ai-development.mdc"; Target = ".cursor\rules\spec-driven-ai-development.mdc" }
    )
    "github-copilot" = @(
        @{ Source = "adapters\github-copilot\.github\copilot-instructions.md"; Target = ".github\copilot-instructions.md" }
    )
    "generic" = @(
        @{ Source = "adapters\generic\AI-SESSION-INSTRUCTIONS.md"; Target = "AI-SESSION-INSTRUCTIONS.md" }
    )
}

foreach ($copy in $copies[$Adapter]) {
    $source = Join-Path $repoRoot $copy.Source
    $target = Join-Path $targetRoot $copy.Target

    if (-not (Test-Path -LiteralPath $source)) {
        throw "Adapter source not found: $source"
    }

    $targetParts = $copy.Target -split '[\\/]'
    $targetDir = $targetRoot
    for ($index = 0; $index -lt $targetParts.Length - 1; $index++) {
        $targetDir = Join-Path $targetDir $targetParts[$index]
        if (Test-Path -LiteralPath $targetDir) {
            $targetDirItem = Get-Item -Force -LiteralPath $targetDir
            if (($targetDirItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
                throw "Refusing to install through linked path: $targetDir"
            }
            if (-not $targetDirItem.PSIsContainer) {
                throw "Adapter target parent is not a directory: $targetDir"
            }
        } else {
            New-Item -ItemType Directory -Path $targetDir | Out-Null
        }
    }

    $targetItem = Get-Item -Force -LiteralPath $target -ErrorAction SilentlyContinue
    if ($targetItem) {
        if (($targetItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
            throw "Refusing to install through linked path: $target"
        }
        if ($targetItem.PSIsContainer) {
            throw "Adapter target is a directory, not a file: $target"
        }
    }

    if ($targetItem -and -not $Force) {
        throw "Target exists: $target. Re-run with -Force to overwrite."
    }

    $stage = Join-Path $targetDir (".sdad-adapter.stage." + [guid]::NewGuid().ToString("N") + ".tmp")
    $backup = $null
    $preserveBackup = $false
    try {
        Copy-Item -LiteralPath $source -Destination $stage -Force
        if ($targetItem -and $targetItem.IsReadOnly) {
            $backup = $stage + ".previous"
            [System.IO.File]::Move($target, $backup)
            try {
                [System.IO.File]::Move($stage, $target)
                $stage = $null
            } catch {
                $replacementError = $_.Exception.Message
                if (-not (Test-Path -LiteralPath $target)) {
                    try {
                        [System.IO.File]::Move($backup, $target)
                        $backup = $null
                    } catch {
                        $preserveBackup = $true
                        throw "Adapter replacement and rollback failed. Previous file retained at $backup. $replacementError"
                    }
                    throw "Adapter replacement failed; the previous file was restored. $replacementError"
                }
                $preserveBackup = $true
                throw "Adapter replacement failed because the target reappeared. Previous file retained at $backup. $replacementError"
            }
            Remove-Item -LiteralPath $backup -Force
            $backup = $null
        } elseif ($targetItem) {
            $backup = $stage + ".previous"
            [System.IO.File]::Replace($stage, $target, $backup)
            $stage = $null
            Remove-Item -LiteralPath $backup -Force
            $backup = $null
        } else {
            [System.IO.File]::Move($stage, $target)
            $stage = $null
        }
    } finally {
        if ($stage -and (Test-Path -LiteralPath $stage)) {
            Remove-Item -LiteralPath $stage -Force
        }
        if (-not $preserveBackup -and $backup -and (Test-Path -LiteralPath $backup)) {
            Remove-Item -LiteralPath $backup -Force
        }
    }
    Write-Host "Installed $Adapter adapter file: $target"
}

Write-Host "Done. Review the installed file and adapt project-specific paths if needed."
