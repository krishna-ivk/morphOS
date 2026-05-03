# P1 Event Taxonomy Spec

## Origin & Influence
- **Source Influence**: `morphOS` event model
- **Local Owner(s)**: `skyforce-core`, `skyforce-symphony`, `skyforce-harness`, `sky-force-command-centre-live`

## Core Concept
The stack requires one universal execution language for observability, human approvals, and deterministic receipts. This prevents different components from emitting vastly different JSON logs that `sky-force-command-centre-live` has to manually decipher.

## Universal Event Structure (`skyforce-core/packages/contracts`)
All state transitions across all repos MUST emit an object implementing the `MorphOSEvent` interface:
```typescript
interface MorphOSEvent {
  event_type: string;
  timestamp: string; // ISO8601
  run_id: string; // Global traceparent identifier
  workspace_id: string; // Bounded context
  payload: any; // Context-specific typing (ExecutionReceipt, ApprovalContext, etc.)
}
```

## Minimum P1 Event Families

### Run Lifecycle
- `factory.manual_run.started`
- `factory.manual_run.completed`
- `run.started`
- `run.blocked`
- `run.completed`
- `run.failed`

### Step execution
- `step.executing`
- `step.completed`
- `step.failed`
- `durable.refresh`
- `durable.resume`
- `durable.cancel`

### Directives & Approvals
- `directive.created`
- `directive.applied`
- `approval.packet.requested`
- `approval.packet.approved`
- `approval.packet.rejected`

### Validation & Summary
- `validation.publish.started`
- `validation.publish.completed`
- `summary.publish.preview`
- `summary.publish.live`

### Promotion & Governed Merge
- `promotion.preview`
- `promotion.apply`
- `promotion.ready`
- `promotion.completed`
- `merge.land.prepared`
- `merge.land.executed`

### Sync & Artifacts
- `sync.issue.started`
- `sync.issue.completed`
- `artifact.created`

## Required Correlation Fields

All `P1` events should carry enough identity to join them later:

- `run_id`
- `issue_identifier`
- `workspace_id`

Step-scoped events should also include:

- `task_execution_id`
- `step_id` inside payload

## Repo Responsibilities

### `skyforce-symphony`

Must emit:

- `run.*`
- `approval.*`
- `promotion.ready`

It owns the orchestration truth of the run.

### `skyforce-harness`

Must emit:

- `step.executing`
- `step.completed`
- `step.failed`
- `validation.*`

It owns the execution truth of the step.

### `sky-force-command-centre-live`

Consumes the canonical event stream to drive real-time operator state, queueing, and approval visibility.

### `skyforce-command-centre`

Should consume the canonical events rather than invent parallel status names.

### `skyforce-core`

Should own the shared event type definitions and any event-ingress helpers.

## P1 Success Condition

`P1` event taxonomy is good enough when:

1. the `P0` golden path can emit a coherent run timeline
2. a human can reconstruct what happened without reading raw process logs
3. the same event names are reused across Symphony, Harness, and Command Centre

## Bottom Line

`P1` event taxonomy is the first observability language of the factory. It should be small, boring, and universal.
