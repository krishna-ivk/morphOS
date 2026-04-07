# P0 Factory Closeout Integration Smoke Runbook

## Purpose

This runbook proves the current factory spine works across the active Skyforce
repos after the closeout hardening wave.

The target line is:

`manual run -> execution receipt -> approval -> promote apply -> promotion branch -> merge handoff -> merge execute`

This is not a unit-test replacement.
It is the operator-grade integration proof that the current `P0`/`P1` closeout
path behaves like one coherent software-factory loop.

## Preconditions

Merged:

- `skyforce-symphony`
- `skyforce-harness`
- `skyforce-core`
- `skyforce-command-centre`
- `skyforce-command-centre-live`

Expected local workspace root:

- `/home/vashista/skyforce`

Suggested smoke issue identifier:

- `REL-SMOKE-001`

## Repo-Level Verification Gate

Run these before the end-to-end smoke:

### `skyforce-symphony`

```bash
cd /home/vashista/skyforce/skyforce-symphony/elixir
mix test test/durable_execution_request_test.exs test/symphony_elixir/workflow_directive_bridge_test.exs
```

### `skyforce-harness`

```bash
cd /home/vashista/skyforce/skyforce-harness
node scripts/test-consume-execution-envelope.mjs
```

### `skyforce-core`

```bash
cd /home/vashista/skyforce/skyforce-core
node scripts/test-promote-apply-materialization.mjs
node scripts/test-land-command.mjs
```

### `skyforce-command-centre`

```bash
cd /home/vashista/skyforce/skyforce-command-centre
./.venv/bin/python -m pytest tests/test_promotions.py tests/test_actions.py tests/test_approval_packets.py tests/test_factory_manual_runs.py tests/test_factory_run_bundle.py tests/test_governed_merge.py tests/test_governed_merge_handoff.py
```

### `skyforce-command-centre-live`

```bash
cd /home/vashista/skyforce/skyforce-command-centre-live
mix precommit
```

Proceed only if all pass.

## Service Startup

### Start FastAPI Command Centre

```bash
cd /home/vashista/skyforce/skyforce-command-centre
./.venv/bin/python main.py
```

### Start Command Centre Live

```bash
cd /home/vashista/skyforce/skyforce-command-centre-live
mix phx.server
```

Useful URLs:

- backend: `http://127.0.0.1:3000`
- LiveView UI: `http://127.0.0.1:4000`

## Step 1 — Launch Manual Factory Run

In the LiveView dashboard:

- operator role: `admin`
- workspace: `workspace-default`
- issue: `REL-SMOKE-001`
- execution mode: choose `factory` or `interactive`
- approval scope: choose `workspace` unless deliberately testing global routing

Submit the manual run form.

Expected result:

- a work order is written
- a run appears in the dashboard
- issue detail is reachable

## Step 2 — Verify Execution Receipt

Query the run bundle:

```bash
cd /home/vashista/skyforce/skyforce-command-centre
curl -s http://127.0.0.1:3000/api/factory/runs/REL-SMOKE-001 | jq
```

Confirm:

- `receipt.status` exists
- `receipt.changed_files` exists
- `receipt.workspace_path` exists
- `receipt.policy_hook` or `receipt.execution.policy_hook` exists when policy was evaluated
- `approval_packet_status` exists
- `required_approver_role` exists

Pass gate:

- receipt exists
- changed-file lineage exists
- runtime policy evidence exists

## Step 3 — Resolve Approval

In issue detail:

- click `Approve Run`

Verify:

```bash
curl -s "http://127.0.0.1:3000/api/operator-action-receipts/latest?issue_identifier=REL-SMOKE-001" | jq
```

Pass gate:

- approval receipt exists
- approval state is approved

## Step 4 — Run Promotion Preview and Apply

From the issue page:

- click `Preview Promotion`
- click `Apply Promotion`

CLI confirmation:

```bash
cd /home/vashista/skyforce/skyforce-core
node scripts/sky.mjs promote-preview --issue REL-SMOKE-001 --json | jq
node scripts/sky.mjs promote-apply --issue REL-SMOKE-001 --json | jq
```

Pass gate:

- promotion apply succeeds
- `proposed_branch` exists in the payload
- branch materialization data exists when live mode is used

## Step 5 — Verify Promotion Branch Exists

Example for `skyforce-core`:

```bash
cd /home/vashista/skyforce/skyforce-core
git rev-parse --verify skyforce/rel-smoke-001-promotion
git log --oneline -1 skyforce/rel-smoke-001-promotion
```

Pass gate:

- the branch exists
- the branch contains the materialized change set

## Step 6 — Prepare Governed Merge Handoff

In issue detail:

- click `Prepare Land Handoff`

Verify:

```bash
curl -s "http://127.0.0.1:3000/api/operator-action-receipts/latest?issue_identifier=REL-SMOKE-001&event_family=merge" | jq
```

Pass gate:

- `merge.handoff.prepare` receipt exists

## Step 7 — Execute Governed Merge

In issue detail:

- click `Execute Land`

CLI confirmation:

```bash
cd /home/vashista/skyforce/skyforce-core
node scripts/sky.mjs land --issue REL-SMOKE-001 --json | jq
git log --oneline main -1
```

Backend confirmation:

```bash
curl -s "http://127.0.0.1:3000/api/operator-action-receipts/latest?issue_identifier=REL-SMOKE-001&event_family=merge" | jq
curl -s "http://127.0.0.1:3000/api/audit/events?issue_identifier=REL-SMOKE-001&event_family=merge" | jq
```

Pass gate:

- `merge.execute` receipt exists
- merge audit event exists
- operator UI shows merged state
- target repo shows the landed change

## Step 8 — Final Operator Surface Check

In the issue page confirm visibility for:

- execution mode
- approval scope
- promotion detail
- governed merge state
- merge detail
- merged/latest operator state

Pass gate:

- an operator can understand the whole closeout path without reading raw files

## Failure Handling

### Approval worked, promotion failed

Check:

```bash
cd /home/vashista/skyforce/skyforce-core
node scripts/sky.mjs promote-preview --issue REL-SMOKE-001 --json | jq
```

Look for:

- missing receipt
- validation not merge-ready
- summary not published
- approval still pending

### Promotion applied, land failed

Check:

```bash
cd /home/vashista/skyforce/skyforce-core
node scripts/sky.mjs land --issue REL-SMOKE-001 --json | jq
git status --short
git branch --list 'skyforce/rel-smoke-001-promotion'
```

Look for:

- dirty target repo
- missing promotion branch
- non-fast-forward condition

### UI state looks stale

Refresh:

```bash
curl -s "http://127.0.0.1:3000/api/factory/runs/REL-SMOKE-001" | jq
curl -s "http://127.0.0.1:3000/api/merges/REL-SMOKE-001/eligibility" | jq
curl -s "http://127.0.0.1:3000/api/merges/REL-SMOKE-001/handoff" | jq
```

## Smoke Success Definition

This smoke is successful only when:

1. manual run launches
2. receipt contains policy and changed-file lineage
3. approval resolves
4. promotion apply succeeds
5. promotion branch exists
6. merge handoff succeeds
7. merge execute succeeds
8. audit and operator receipts exist
9. operator UI shows merged final state

## Current Constraints

The current closeout path is still intentionally narrow:

- local topology assumptions remain
- landing is fast-forward only
- policy logic is still repo-local rather than one shared cross-repo policy engine

Even so, if every gate above passes, the current factory closeout path is
credible enough for the present milestone.
