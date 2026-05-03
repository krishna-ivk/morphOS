# Durable Work Ledger Spec

## Purpose

The **Durable Work Ledger** turns ephemeral execution artifacts (receipts, approvals, promotions, events) into a governed, survivable, and branch-aware record of work. Inspired by `beadwork`, it provides the "single source of truth" for the current state and audit history of any issue or work order in the factory.

## Why This Matters

Current P1/V1 relies on split artifact streams:
- `.agent-status/` (JSON files)
- `.symphony-workspaces/` (JSON envelopes and validation summaries)
- `operator-action-receipts.json` (Local API store)
- `audit-events.json` (Local API store)

The **Durable Work Ledger** unifies these by treating the **Work Ledger Repository** (or a specialized ledger service) as the primary storage layer, rather than ad-hoc JSON files.

## Core Structure

A canonical `WorkLedgerEntry` (defined in `skyforce-core` contracts) includes:

- `ledger_id`: Unique identifier for the ledger instance (typically tied to an issueID).
- `sequence_id`: Monotonically increasing sequence or timestamp.
- `entry_type`: `work_order` | `directive` | `run_envelope` | `receipt` | `approval` | `promotion` | `validation` | `outcome`.
- `event_taxonomy`: Canonical MorphOS event category.
- `payload`: The actual message/artifact data (e.g., the `ExecutionReceipt`).
- `metadata`: Source node, operator identity, signature, and authority scope.
- `hash`: SHA-256 hash or parent hash (for chainable ledgers).
- `recorded_at`: ISODateTime.

## Git-Native Mode (Beadwork-inspired)

In the software factory, the ledger should eventually be implemented using **Git-Native** storage:
1. Each `issue-identifier` has a dedicated branch or object stream in the `skyforce-work-ledger` repository.
2. Every significant action (approval, materialization, land) results in a signed commit.
3. The "Work Summary" and "Run Bundle" are projected from the current tip of the ledger branch.

## Implementation Seams

### 1. `skyforce-core` (Contracts)
Define the `WorkLedgerEntry` and `WorkLedgerSnapshot` interfaces.

### 2. `skyforce-api-gateway` (Ledger Service)
Move from locally appending to `operator-audit-store.json` to a `DurableLedgerRepository` that persists entries in the governed ledger structure.

### 3. `skyforce-symphony` (Checkpoint Trigger)
Symphony should "flush" its current internal run state to the durable ledger upon reaching specific task-state transitions (e.g., `run.blocked`, `run.completed`).

### 4. `morphOS` (Ledger Schema)
Define the canonical mapping between different artifact kinds and their ledger entry types.

## Benefits

- **Survivability**: Run state can be recovered even if a symphony node crashes.
- **Auditability**: Complete, tamper-evident history of operator and agent actions.
- **Projectability**: Command Centre can rebuild the "current truth" for any issue by replaying the ledger.
- **Branch-Awareness**: Work ledgers naturally follow the lifecycle of feature branches.
