# Machine Roles — Non-Human Actors in the Symbiosis

---

## CI/CD System

### Identity

```yaml
name: cicd_system
title: CI/CD System
category: machine
organism_analogy: The reflex arc — automated stimulus-response without conscious thought
```

### Contributions

```yaml
contributions:
  - name: build_triggers
    format: webhook
    schema_ref: freeform
    frequency: on_event
    criticality: important
    description: Triggers pipelines on code push, PR, or schedule

  - name: build_artifacts
    format: file
    schema_ref: freeform
    frequency: per_build
    criticality: important
    description: Compiled binaries, container images, release packages

  - name: build_status
    format: json
    schema_ref: freeform
    frequency: per_build
    criticality: critical
    description: Pass/fail status that gates deployment
```

### Consumes

```yaml
consumes:
  - name: deploy_request
    format: json
    source: orchestrator (via deploy.sh)
    frequency: per_release

  - name: code_patches
    format: diff
    source: coding_agent
    frequency: per_task
```

### Integration Contract

```yaml
integration:
  inbound: webhook → interaction_layer → orchestrator
  outbound: deploy.sh → CI/CD API
  auth: API key or OIDC token
  connectivity_requires: online_write
```

---

## External Agents (Hermes, Other OS Instances)

### Identity

```yaml
name: external_agent
title: External Agent / Partner OS
category: machine
organism_analogy: Symbiotic organisms — separate life forms that cooperate for mutual benefit
```

### Contributions

```yaml
contributions:
  - name: delegated_task_results
    format: json
    schema_ref: docs/schemas.md#task_item
    frequency: on_event
    criticality: important
    description: Completed work from tasks this OS delegated to the external agent

  - name: cross_system_events
    format: json
    schema_ref: docs/schemas.md#event_envelope
    frequency: on_event
    criticality: enhancing
    description: Events from other system instances (shared learning, alerts)

  - name: shared_capability_entries
    format: json
    schema_ref: docs/schemas.md#capability_store
    frequency: on_demand
    criticality: enhancing
    description: Patterns and fixes discovered by peer OS instances
```

### Consumes

```yaml
consumes:
  - name: delegated_tasks
    format: json
    source: orchestrator (tasks too large or specialized for this instance)
    frequency: on_demand

  - name: sync_requests
    format: json
    source: connectivity_manager
    frequency: on_connectivity
```

### Integration Contract

```yaml
integration:
  inbound: HTTPS/WebSocket → event_bus
  outbound: event_bus → HTTPS to peer
  auth: API key (mutual)
  connectivity_requires: online_read
```

---

## Monitoring System

### Identity

```yaml
name: monitoring_system
title: Monitoring System (Prometheus, Datadog, etc.)
category: machine
organism_analogy: The medical instruments — EKG, blood pressure monitor, thermometer
```

### Contributions

```yaml
contributions:
  - name: anomaly_alerts
    format: notification
    schema_ref: freeform
    frequency: on_event
    criticality: important
    description: Fires alerts when health metrics exceed thresholds

  - name: metric_aggregation
    format: dashboard
    schema_ref: freeform
    frequency: continuous
    criticality: enhancing
    description: Historical trend data for performance analysis
```

### Consumes

```yaml
consumes:
  - name: agent_health_reports
    format: json
    source: event_bus (agent.health events)
    frequency: continuous

  - name: resource_usage_metrics
    format: json
    source: health_reports.resource_usage
    frequency: continuous

  - name: event_throughput
    format: metrics
    source: event_bus
    frequency: continuous
```

### Integration Contract

```yaml
integration:
  inbound: scrape agent.health events from event_bus or /metrics endpoint
  outbound: alert webhook → interaction_layer
  auth: internal network (no auth) or API key
  connectivity_requires: none (can run locally)
```

---

## Ticketing System (Linear, Jira)

### Identity

```yaml
name: ticketing_system
title: Ticketing System
category: machine
organism_analogy: The postal system — delivers orders to organs and reports back delivery status
```

### Contributions

```yaml
contributions:
  - name: task_tickets
    format: json
    schema_ref: freeform
    frequency: on_event
    criticality: important
    description: Work items created by humans that become OS jobs

  - name: priority_labels
    format: json
    schema_ref: freeform
    frequency: on_event
    criticality: enhancing
    description: Priority and label metadata that influence task ordering

  - name: sprint_boundaries
    format: json
    schema_ref: freeform
    frequency: per_sprint
    criticality: enhancing
    description: Which tickets are in scope for the current iteration
```

### Consumes

```yaml
consumes:
  - name: task_status_updates
    format: json
    source: orchestrator (task.completed, task.failed events)
    frequency: per_task

  - name: run_summaries
    format: markdown
    source: orchestrator
    frequency: per_run

  - name: escalation_events
    format: json
    source: event_bus (agent.escalate)
    frequency: on_event
```

### Integration Contract

```yaml
integration:
  inbound: webhook (ticket created/updated) → interaction_layer
  outbound: orchestrator → ticketing API (status sync, comments)
  auth: API key or OAuth
  connectivity_requires: online_write
```
