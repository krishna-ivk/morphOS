# Event Bus Specification — The Nervous System

## Purpose

The event bus is the **nervous system** of SkyForce. It is the only
sanctioned way for agents to communicate with each other. No agent may
call another agent directly. All signals pass through the bus.

---

## Design Principles

1. **Publish / Subscribe** — agents emit events; interested agents listen
2. **Asynchronous by default** — emitting an event does not block the sender
3. **Envelope format** — every message uses the standard event envelope from `docs/schemas.md`
4. **At-least-once delivery** — events may be delivered more than once; consumers must be idempotent
5. **Ordered per source** — events from the same agent arrive in emission order
6. **Durable when offline** — events are persisted to disk before acknowledgment

---

## Event Taxonomy

Events follow a `domain.action` naming convention.

### Workflow Events

| Event Type | Source | Description |
|---|---|---|
| `workflow.started` | orchestrator | A new workflow run has begun |
| `workflow.step.started` | orchestrator | A specific step is about to execute |
| `workflow.step.completed` | orchestrator | A step finished successfully |
| `workflow.step.failed` | orchestrator | A step failed |
| `workflow.completed` | orchestrator | Entire workflow finished |
| `workflow.paused` | orchestrator | Workflow paused (connectivity loss, policy block) |

### Agent Events

| Event Type | Source | Description |
|---|---|---|
| `agent.activated` | any agent | Agent has started processing |
| `agent.health` | any agent | Periodic heartbeat with health report |
| `agent.completed` | any agent | Agent finished its work successfully |
| `agent.failed` | any agent | Agent failed and cannot recover |
| `agent.escalate` | any agent | Agent needs human or orchestrator help |

### Task Events

| Event Type | Source | Description |
|---|---|---|
| `task.created` | orchestrator | A new task was added to the queue |
| `task.assigned` | orchestrator | A task was assigned to an agent |
| `task.completed` | coding_agent | Implementation and tests done |
| `task.failed` | coding_agent | Implementation could not be completed |

### Test Events

| Event Type | Source | Description |
|---|---|---|
| `test.started` | run_tests.sh | Test suite is running |
| `test.passed` | run_tests.sh | All tests passed |
| `test.failed` | run_tests.sh | One or more tests failed |

### Learning Events

| Event Type | Source | Description |
|---|---|---|
| `pattern.discovered` | learning_agent | A new reusable pattern was found |
| `fix.recorded` | learning_agent | A bug fix was added to the capability store |
| `lesson.recorded` | learning_agent | An architecture lesson was stored |

### Connectivity Events

| Event Type | Source | Description |
|---|---|---|
| `connectivity.online` | connectivity_manager | Internet became available |
| `connectivity.offline` | connectivity_manager | Internet was lost |
| `connectivity.mode_changed` | connectivity_manager | Capability flags changed |

### Policy Events

| Event Type | Source | Description |
|---|---|---|
| `policy.violation` | policy_engine | An action was blocked by policy |
| `policy.warning` | policy_engine | An action is allowed but risky |
| `policy.approved` | policy_engine | An action passed policy checks |

---

## Subscription Rules

Each agent declares its subscriptions in its agent definition under `events.listens_to`.
The orchestrator subscribes to **all** events for workflow coordination.

### Routing Examples

```
vision_agent    → emits: task.created
                → listens: workflow.step.started

coding_agent    → emits: task.completed, task.failed
                → listens: task.assigned, pattern.discovered

debugging_agent → emits: task.completed, fix.recorded
                → listens: test.failed

architecture_agent → emits: agent.completed
                   → listens: workflow.step.started

learning_agent  → emits: pattern.discovered, fix.recorded, lesson.recorded
                → listens: workflow.completed, task.completed, test.failed
```

---

## Persistence Layer

Events are stored in `logs/events/` as newline-delimited JSON files:

```
logs/events/2026-03-13.ndjson
```

Each line is one event envelope. This enables:
- Post-mortem analysis of any workflow run
- Replay of events for debugging
- Feeding the learning agent with historical data

---

## Deferred Event Queue

When the system is offline, events targeting online-only consumers are
stored in `runtime/deferred_events.json`. When connectivity returns:

1. `connectivity_manager` emits `connectivity.online`
2. Orchestrator reads `deferred_events.json`
3. Each deferred event is re-emitted in original order
4. The deferred queue is cleared

---

## Error Handling

- **Undeliverable events** (no subscribers): logged as warnings, not errors
- **Consumer crashes**: event is requeued for retry (max 3 attempts)
- **Poison messages** (repeated consumer failure): moved to `logs/dead_letters/`
- **Bus overload**: backpressure signal sent; producers slow down via cooldown
