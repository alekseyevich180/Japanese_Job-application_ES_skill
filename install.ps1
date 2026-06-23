$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$SourceRoot = Join-Path $ProjectRoot "skills"

if ($env:CODEX_HOME) {
    $CodexHome = $env:CODEX_HOME
} else {
    $CodexHome = Join-Path $HOME ".codex"
}

$TargetRoot = Join-Path $CodexHome "skills"

New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null

Get-ChildItem -Path $SourceRoot -Directory | ForEach-Object {
    $Source = $_.FullName
    $Target = Join-Path $TargetRoot $_.Name

    if (Test-Path $Target) {
        Remove-Item -LiteralPath $Target -Recurse -Force
    }

    Copy-Item -Path $Source -Destination $Target -Recurse
    Write-Host "Installed $($_.Name) to $Target"
}

Write-Host "Restart Codex or start a new session to use the skill."
