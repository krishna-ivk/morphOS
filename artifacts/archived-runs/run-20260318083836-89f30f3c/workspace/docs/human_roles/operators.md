# Operator Roles — Those Who Keep the Organism Alive

---

## Platform Admin

### Identity

```yaml
name: platform_admin
title: Platform Administrator
category: operator
organism_analogy: The surgeon — installs, transplants, and maintains the physical body
```

### Contributions

```yaml
contributions:
  - name: infrastructure_config
    format: yaml
    schema_ref: freeform
    frequency: per_project
    criticality: critical
    description: Docker configs, server provisioning, resource limits

  - name: os_upgrades
    format: file
    schema_ref: freeform
    frequency: on_demand
    criticality: important
    description: Deploys new versions of the OS runtime itself

  - name: resource_scaling
    format: yaml
    schema_ref: freeform
    frequency: on_demand
    criticality: important
    description: Adjusts CPU, memory, and concurrency limits based on workload

  - name: backup_restore
    format: file
    schema_ref: freeform
    frequency: on_demand
    criticality: critical
    description: Backup and recovery of memory, logs, and configuration
```

### Consumes

```yaml
consumes:
  - name: system_health_dashboard
    format: dashboard
    source: health_reports from all agents
    frequency: continuous

  - name: resource_utilization
    format: metrics
    source: runtime infrastructure
    frequency: continuous

  - name: dead_letters
    format: ndjson
    source: logs/dead_letters/
    frequency: daily
```

### Interfaces

```yaml
interfaces:
  - name: infrastructure_cli
    type: cli
    permission: write
    description: docker-compose, kubernetes, or bare-metal management

  - name: config_files
    type: file_system
    permission: write
    description: Edit runtime configuration, resource limits, connectivity settings

  - name: monitoring_dashboard
    type: web_ui
    permission: read
    description: Real-time system metrics and alerting
```

### Triggers

```yaml
triggered_by:
  - event_type: system.out_of_resources
    urgency: immediate
    action: Scale up resources or kill non-essential processes

  - event_type: system.crash
    urgency: immediate
    action: Restart the OS, restore from checkpoint

  - event_type: connectivity.offline (persistent)
    urgency: next_session
    action: Diagnose network issues
```

### Absence Impact

```yaml
absence_impact:
  - scenario: OS instance dies with no admin to restart
    consequence: All pipelines halt; no new work can be accepted
    mitigation: Auto-restart via systemd/Docker restart policies

  - scenario: Resources exhausted with no scaling response
    consequence: Agents get killed by budget enforcement; throughput drops to zero
    mitigation: Conservative default resource limits; alert escalation chain
```

### Evolution Contribution

```yaml
evolution:
  feeds: infrastructure patterns, resource scaling heuristics
  mechanism: >
    Resource adjustments over time teach the OS optimal default configurations.
    Platform configs that work well are stored as templates for future deployments.
```

---

## Policy Author

### Identity

```yaml
name: policy_author
title: Policy Author
category: operator
organism_analogy: The immunologist — programs the immune system's rules for threat detection
```

### Contributions

```yaml
contributions:
  - name: policy_rules
    format: yaml
    schema_ref: docs/policy_engine_spec.md
    frequency: on_demand
    criticality: critical
    description: Safety rules that gate every action in the system

  - name: threat_model_updates
    format: markdown
    schema_ref: freeform
    frequency: per_project
    criticality: important
    description: New threat types and detection patterns

  - name: policy_tuning
    format: yaml
    schema_ref: docs/policy_engine_spec.md
    frequency: on_demand
    criticality: important
    description: Adjusting rule sensitivity (tightening or loosening thresholds)
```

### Consumes

```yaml
consumes:
  - name: policy_violation_log
    format: ndjson
    source: logs/policy_violations.ndjson
    frequency: daily

  - name: false_positive_reports
    format: notification
    source: agents (when policy rejects valid work)
    frequency: on_event

  - name: quarantined_outputs
    format: file
    source: artifacts/quarantine/
    frequency: on_event
```

### Interfaces

```yaml
interfaces:
  - name: policy_file_editor
    type: file_system
    permission: write
    description: Create and edit policies/*.yaml

  - name: violation_viewer
    type: web_ui
    permission: read
    description: Browse violation history, identify patterns

  - name: policy_test_cli
    type: cli
    permission: execute
    description: Dry-run policies against historical data to check for false positives
```

### Triggers

```yaml
triggered_by:
  - event_type: policy.violation (recurring, same rule)
    urgency: next_session
    action: Investigate if rule is too strict (false positive) or agents keep misbehaving

  - event_type: security_incident
    urgency: immediate
    action: Write emergency policy rule to block the attack vector
```

### Absence Impact

```yaml
absence_impact:
  - scenario: No policy rules beyond core_safety
    consequence: Only baseline protections; project-specific risks uncovered
    mitigation: core_safety.yaml provides essential guardrails by default

  - scenario: False positives never tuned
    consequence: Agents waste retries on policy rejections; throughput drops
    mitigation: learning_agent flags recurring violations for review
```

### Evolution Contribution

```yaml
evolution:
  feeds: policy_memory, immune system maturity
  mechanism: >
    Every policy rule written is a permanent immune upgrade. Policy tuning
    based on violation logs creates an adaptive immune system that gets
    smarter about distinguishing real threats from false alarms.
```

---

## DevOps / SRE

### Identity

```yaml
name: devops_sre
title: DevOps / Site Reliability Engineer
category: operator
organism_analogy: The cardiologist — monitors vital signs and ensures continuous blood flow
```

### Contributions

```yaml
contributions:
  - name: deployment_pipelines
    format: yaml
    schema_ref: freeform
    frequency: per_project
    criticality: important
    description: CI/CD configurations the deploy.sh integrates with

  - name: monitoring_setup
    format: yaml
    schema_ref: freeform
    frequency: per_project
    criticality: important
    description: Alert rules, health check endpoints, log aggregation config

  - name: incident_response
    format: natural_language
    schema_ref: freeform
    frequency: on_escalation
    criticality: critical
    description: Hands-on fixing when the OS or deployed apps have production issues

  - name: dead_letter_resolution
    format: natural_language
    schema_ref: freeform
    frequency: daily
    criticality: enhancing
    description: Review and resolve poison messages that the event bus couldn't deliver
```

### Consumes

```yaml
consumes:
  - name: agent_health_reports
    format: json
    source: all agents (via event_bus)
    frequency: continuous

  - name: event_logs
    format: ndjson
    source: logs/events/
    frequency: on_demand

  - name: dead_letters
    format: ndjson
    source: logs/dead_letters/
    frequency: daily

  - name: deployment_status
    format: json
    source: deploy.sh
    frequency: per_deployment
```

### Interfaces

```yaml
interfaces:
  - name: log_viewer
    type: cli
    permission: read
    description: Tail and search event logs, health reports, violations

  - name: alerting_system
    type: notification
    permission: read
    description: Receive alerts on agent failures, resource exhaustion, dead letters

  - name: deployment_cli
    type: cli
    permission: execute
    description: Manual deployment triggers and rollbacks
```

### Triggers

```yaml
triggered_by:
  - event_type: agent.health (status: failing or dead)
    urgency: immediate
    action: Investigate agent crash, check resource limits, restart if needed

  - event_type: system.dead_letter_threshold
    urgency: next_session
    action: Review and resolve accumulated dead letters

  - event_type: deployment.failed
    urgency: immediate
    action: Diagnose deploy failure, rollback if needed
```

### Absence Impact

```yaml
absence_impact:
  - scenario: Agent crashes with no one monitoring health
    consequence: Orchestrator retries; if all retries fail, pipeline stalls silently
    mitigation: Auto-restart policies; health dashboard with email alerts

  - scenario: Dead letters accumulate unreviewd
    consequence: Lost events may mean missed learning or missed failures
    mitigation: Periodic automated dead letter report
```

### Evolution Contribution

```yaml
evolution:
  feeds: reliability patterns, deployment stability data
  mechanism: >
    Incident responses and dead letter resolutions teach the OS what failure
    modes are most common and how to self-recover. Monitoring configs that
    catch issues early become standard health check patterns.
```

---

## Secret Manager

### Identity

```yaml
name: secret_manager
title: Secret Manager
category: operator
organism_analogy: The thymus — trains the immune system on what is "self" vs "foreign"
```

### Contributions

```yaml
contributions:
  - name: credential_vault
    format: file
    schema_ref: freeform
    frequency: per_project
    criticality: critical
    description: Secure storage of API keys, database passwords, deploy tokens

  - name: key_rotation
    format: file
    schema_ref: freeform
    frequency: periodic
    criticality: critical
    description: Regular rotation of all credentials to limit exposure window

  - name: secret_detection_patterns
    format: yaml
    schema_ref: freeform
    frequency: on_demand
    criticality: important
    description: Regex patterns for new secret types (added to policy_engine)
```

### Consumes

```yaml
consumes:
  - name: secret_leak_alerts
    format: notification
    source: policy_engine (block_secret_in_code)
    frequency: on_event

  - name: policy_violation_log
    format: ndjson
    source: logs/policy_violations.ndjson (secret-related entries)
    frequency: weekly
```

### Interfaces

```yaml
interfaces:
  - name: vault
    type: api
    permission: write
    description: Manage secrets in a vault (HashiCorp, AWS Secrets Manager, etc.)

  - name: env_file_editor
    type: file_system
    permission: write
    description: Configure .env files that agents reference (never committed to repo)
```

### Triggers

```yaml
triggered_by:
  - event_type: policy.violation (rule: block_secret_in_code)
    urgency: immediate
    action: Rotate the exposed credential; update vault

  - event_type: credential.expiring
    urgency: next_session
    action: Rotate before expiry to prevent pipeline breakage
```

### Absence Impact

```yaml
absence_impact:
  - scenario: No credentials configured
    consequence: Agents cannot connect to databases, APIs, or deploy targets
    mitigation: Pipeline runs in local-only mode; online features unavailable

  - scenario: Leaked secret not rotated
    consequence: Security exposure persists; policy blocks future deploys
    mitigation: policy_engine blocks all deploys until secret is rotated
```

### Evolution Contribution

```yaml
evolution:
  feeds: secret detection patterns in policy_engine
  mechanism: >
    New secret patterns (custom API key formats) are added to the
    block_secret_in_code rule. Each rotation event teaches the OS
    which credentials exist and how frequently they change.
```
