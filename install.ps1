$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Source = Join-Path $ProjectRoot "skills\japanese-es-writing"

if ($env:CODEX_HOME) {
    $CodexHome = $env:CODEX_HOME
} else {
    $CodexHome = Join-Path $HOME ".codex"
}

$TargetRoot = Join-Path $CodexHome "skills"
$Target = Join-Path $TargetRoot "japanese-es-writing"

New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null

if (Test-Path $Target) {
    Remove-Item -LiteralPath $Target -Recurse -Force
}

Copy-Item -Path $Source -Destination $Target -Recurse

Write-Host "Installed japanese-es-writing to $Target"
Write-Host "Restart Codex or start a new session to use the skill."
