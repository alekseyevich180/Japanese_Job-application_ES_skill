$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillNames = @(
    "japanese-es-writing",
    "nature-polishing",
    "nature-writing"
)

if ($env:CODEX_HOME) {
    $CodexHome = $env:CODEX_HOME
} else {
    $CodexHome = Join-Path $HOME ".codex"
}

$TargetRoot = Join-Path $CodexHome "skills"

New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null

foreach ($SkillName in $SkillNames) {
    $Source = Join-Path $ProjectRoot "skills\$SkillName"
    $Target = Join-Path $TargetRoot $SkillName

    if (-not (Test-Path $Source)) {
        throw "Skill source not found: $Source"
    }

    if (Test-Path $Target) {
        Remove-Item -LiteralPath $Target -Recurse -Force
    }

    Copy-Item -Path $Source -Destination $Target -Recurse
    Write-Host "Installed $SkillName to $Target"
}

Write-Host "Restart Codex or start a new session to use the skill."
