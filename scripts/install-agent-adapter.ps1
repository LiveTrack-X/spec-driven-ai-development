param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("codex", "claude-code", "cursor", "github-copilot", "generic")]
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
    $targetDir = Split-Path -Parent $target

    if (-not (Test-Path -LiteralPath $source)) {
        throw "Adapter source not found: $source"
    }

    if ((Test-Path -LiteralPath $target) -and -not $Force) {
        throw "Target exists: $target. Re-run with -Force to overwrite."
    }

    if ($targetDir -and -not (Test-Path -LiteralPath $targetDir)) {
        New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
    }

    Copy-Item -LiteralPath $source -Destination $target -Force:$Force
    Write-Host "Installed $Adapter adapter file: $target"
}

Write-Host "Done. Review the installed file and adapt project-specific paths if needed."
