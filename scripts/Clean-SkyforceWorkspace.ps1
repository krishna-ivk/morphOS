param(
    [switch]$All
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$workspaceRoot = Split-Path -Parent $PSScriptRoot
$tmpRoot = Join-Path $workspaceRoot "tmp-workspaces"
$knownMissionIds = @(
    "mission-skyforce-demo",
    "mission-gcloud-edge-runbook",
    "mission-agentic-handoff"
)

if (-not (Test-Path -LiteralPath $tmpRoot)) {
    Write-Host "No tmp-workspaces directory found."
    return
}

$targets = if ($All) {
    @(Get-ChildItem -LiteralPath $tmpRoot -Directory)
}
else {
    @(
        foreach ($missionId in $knownMissionIds) {
            $missionPath = Join-Path $tmpRoot $missionId
            if (Test-Path -LiteralPath $missionPath) {
                Get-Item -LiteralPath $missionPath
            }
        }
    )
}

if ($targets.Count -eq 0) {
    Write-Host "No generated mission workspaces matched the cleanup scope."
    return
}

foreach ($target in $targets) {
    Remove-Item -LiteralPath $target.FullName -Recurse -Force
    Write-Host ("Removed : {0}" -f $target.FullName)
}

Write-Host ""
Write-Host "Workspace cleanup complete."
