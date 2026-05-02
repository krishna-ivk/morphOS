param(
    [string[]]$MissionPaths = @(
        (Join-Path $PSScriptRoot "..\skyforce-core\data\sample-mission.json"),
        (Join-Path $PSScriptRoot "..\skyforce-core\data\gcloud-edge-runbook-mission.json"),
        (Join-Path $PSScriptRoot "..\skyforce-core\data\agentic-handoff-mission.json")
    )
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$workspaceRoot = Split-Path -Parent $PSScriptRoot
$demoScript = Join-Path $workspaceRoot "skyforce-command-centre\Start-SkyforceDemo.ps1"
$assetValidationScript = Join-Path $PSScriptRoot "Validate-SkyforceAssets.ps1"

Write-Host ""
Write-Host "SKYFORCE WORKSPACE VERIFY"
Write-Host "========================="

& $assetValidationScript

foreach ($missionPath in $MissionPaths) {
    $resolvedMissionPath = (Resolve-Path -LiteralPath $missionPath).Path
    $mission = Get-Content -LiteralPath $resolvedMissionPath -Raw | ConvertFrom-Json
    $missionWorkspace = Join-Path $workspaceRoot ("tmp-workspaces\{0}" -f $mission.mission_id)
    $reportPath = Join-Path $missionWorkspace "operator-report.md"
    $timelinePath = Join-Path $missionWorkspace "timeline.json"

    Write-Host ""
    Write-Host ("Mission  : {0}" -f $mission.summary)
    & $demoScript -MissionPath $resolvedMissionPath | Out-Null

    if (-not (Test-Path -LiteralPath $reportPath)) {
        throw "Expected operator report was not written for mission '$($mission.mission_id)'."
    }

    if (-not (Test-Path -LiteralPath $timelinePath)) {
        throw "Expected timeline was not written for mission '$($mission.mission_id)'."
    }

    $timeline = Get-Content -LiteralPath $timelinePath -Raw | ConvertFrom-Json
    if ($timeline.final_status -ne "succeeded") {
        throw "Mission '$($mission.mission_id)' did not succeed. Final status: $($timeline.final_status)"
    }

    Write-Host ("Result   : succeeded ({0})" -f $mission.mission_id)
}

Write-Host ""
Write-Host "Workspace verification passed."
