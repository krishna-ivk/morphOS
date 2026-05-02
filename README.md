# Skyforce Workspace

This workspace is a local PowerShell vertical slice of Skyforce.

Skyforce in this repo is one coherent flow:
- `skyforce-core` defines shared contracts, workflow resolution, and JSON helpers.
- `skyforce-symphony` plans a mission and produces an execution envelope.
- `skyforce-harness` simulates execution and emits typed timeline events.
- `skyforce-command-centre` runs the end-to-end demo and writes the operator report.

## What This Prototype Proves

This workspace is focused on a narrow, realistic slice:
- mission intake from JSON
- capability-aware routing
- workflow-template or runbook resolution
- execution-envelope handoff
- timeline generation
- operator-facing report output

It is not a full production Skyforce runtime. It is the smallest coherent local model of the planner -> executor -> operator loop.

## Run The Demo

From the workspace root:

```powershell
powershell -ExecutionPolicy Bypass -File .\skyforce-command-centre\Start-SkyforceDemo.ps1
```

Optional failover simulation:

```powershell
powershell -ExecutionPolicy Bypass -File .\skyforce-command-centre\Start-SkyforceDemo.ps1 -SimulateFailover
```

Optional mission input:

```powershell
powershell -ExecutionPolicy Bypass -File .\skyforce-command-centre\Start-SkyforceDemo.ps1 -MissionPath .\skyforce-core\data\sample-mission.json
```

## Verify The Workspace

Run the full local smoke check:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\Verify-SkyforceWorkspace.ps1
```

Validate contracts, templates, and mission inputs only:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\Validate-SkyforceAssets.ps1
```

Clean generated mission outputs for the built-in demo missions:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\Clean-SkyforceWorkspace.ps1
```

Clean every generated workspace under `tmp-workspaces`:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\Clean-SkyforceWorkspace.ps1 -All
```

## Repo Roles

### `skyforce-core`
- shared PowerShell module
- mission workflow resolution
- contract catalog loading
- execution-envelope and timeline-event helpers

### `skyforce-symphony`
- mission planning
- node selection
- approval-gate shaping
- plan and envelope generation

### `skyforce-harness`
- execution simulation
- timeline emission
- failover simulation
- final mission result generation

### `skyforce-command-centre`
- operator-facing entrypoint
- console summary
- report generation

## Output Paths

Generated workspace artifacts are written under:

```text
tmp-workspaces/<mission-id>/
```

Typical outputs:
- `plan.json`
- `execution-envelope.json`
- `timeline.json`
- `operator-report.md`

## Current Constraints

The current local slice is intentionally limited:
- execution is simulated, not connected to real external runners
- approval is modeled as dry-run acknowledgement
- policy evaluation is descriptive, not enforcing external side effects
- reporting is file-based, not a live UI

That constraint is a strength here: the prototype stays small, legible, and runnable.
