Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$workspaceRoot = Split-Path -Parent $PSScriptRoot
$coreRoot = Join-Path $workspaceRoot "skyforce-core"
$contractRoot = Join-Path $coreRoot "contracts"
$templateRoot = Join-Path $coreRoot "templates"
$missionRoot = Join-Path $coreRoot "data"
$modulePath = Join-Path $coreRoot "Skyforce.Core.psm1"

Import-Module $modulePath -Force

Write-Host ""
Write-Host "SKYFORCE ASSET VALIDATION"
Write-Host "========================="

foreach ($contractFile in @(Get-ChildItem -LiteralPath $contractRoot -File -Filter *.json | Sort-Object Name)) {
    $contract = Read-SkyforceJson -Path $contractFile.FullName
    foreach ($field in @("contract_id", "version")) {
        if ($null -eq $contract.PSObject.Properties[$field] -or [string]::IsNullOrWhiteSpace([string]$contract.$field)) {
            throw "Contract '$($contractFile.Name)' is missing required field '$field'."
        }
    }

    Write-Host ("Contract : ok ({0})" -f $contractFile.Name)
}

foreach ($templateFile in @(Get-ChildItem -LiteralPath $templateRoot -File -Filter *.json | Sort-Object Name)) {
    $template = Read-SkyforceWorkflowTemplate -TemplatePath $templateFile.FullName
    Test-SkyforceWorkflowTemplate -Template $template | Out-Null
    Write-Host ("Template : ok ({0})" -f $templateFile.Name)
}

foreach ($missionFile in @(Get-ChildItem -LiteralPath $missionRoot -File -Filter *.json | Sort-Object Name)) {
    $mission = Read-SkyforceJson -Path $missionFile.FullName
    $workflow = Resolve-SkyforceMissionWorkflow -Mission $mission
    $steps = @($workflow.steps)

    if ($steps.Count -eq 0) {
        throw "Mission '$($missionFile.Name)' resolved to zero workflow steps."
    }

    Write-Host ("Mission   : ok ({0} -> {1}, {2} steps)" -f $missionFile.Name, $workflow.source, $steps.Count)
}

Write-Host ""
Write-Host "Asset validation passed."
