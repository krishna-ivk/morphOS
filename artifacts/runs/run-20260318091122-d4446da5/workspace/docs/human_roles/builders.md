# Builder Roles — Those Who Evolve the Organism

---

## Agent Developer

### Identity

```yaml
name: agent_developer
title: Agent Developer
category: builder
organism_analogy: The stem cell engineer — creates new specialized cells from the base template
```

### Contributions

```yaml
contributions:
  - name: new_agent_definitions
    format: markdown
    schema_ref: docs/cell_spec.md
    frequency: on_demand
    criticality: critical
    description: New agents grown from cell_spec.md — adds new capabilities to the OS

  - name: agent_upgrades
    format: markdown
    schema_ref: docs/cell_spec.md
    frequency: on_demand
    criticality: important
    description: Version bumps to existing agents — new failure modes, tools, or behavior

  - name: agent_test_suites
    format: file
    schema_ref: freeform
    frequency: per_agent
    criticality: important
    description: Test scenarios validating agent behavior against spec
```

### Consumes

```yaml
consumes:
  - name: cell_spec_template
    format: markdown
    source: docs/cell_spec.md
    frequency: per_agent

  - name: agent_health_history
    format: ndjson
    source: logs/events/ (agent.health)
    frequency: on_demand

  - name: capability_gaps
    format: notification
    source: orchestrator (when no agent can handle a task type)
    frequency: on_event
```

### Interfaces

```yaml
interfaces:
  - name: agent_file_editor
    type: file_system
    permission: write
    description: Create/edit docs/agents/*.md files

  - name: agent_test_runner
    type: cli
    permission: execute
    description: Run validation tests against agent definitions
```

### Triggers

```yaml
triggered_by:
  - event_type: orchestrator.no_capable_agent
    urgency: next_session
    action: Build a new agent for the unhandled task type

  - event_type: agent.health (status: failing, recurring)
    urgency: next_session
    action: Investigate and upgrade the struggling agent
```

### Absence Impact

```yaml
absence_impact:
  - scenario: No new agents ever created
    consequence: OS cannot grow beyond its initial 5 capabilities
    mitigation: Existing agents handle broader scope (but with lower quality)

  - scenario: Agents never upgraded
    consequence: Same failure modes repeat; no improvement in agent behavior
    mitigation: learning_agent suggestions pile up as recommendations
```

### Evolution Contribution

```yaml
evolution:
  feeds: organism capability breadth, agent quality
  mechanism: >
    Every new agent is a new organ. Every agent upgrade is a mutation that
    makes the organism more adapted. The agent developer is the primary
    driver of the OS's long-term evolution.
```

---

## Schema Author

### Identity

```yaml
name: schema_author
title: Schema Author
category: builder
organism_analogy: The geneticist who edits DNA — changes the fundamental language cells use to communicate
```

### Contributions

```yaml
contributions:
  - name: schema_definitions
    format: json_schema
    schema_ref: docs/schemas.md
    frequency: on_demand
    criticality: critical
    description: JSON schemas that define all inter-component data contracts

  - name: schema_migrations
    format: markdown
    schema_ref: freeform
    frequency: on_demand
    criticality: important
    description: Migration guides when schemas change (backward compatibility handling)

  - name: schema_validation_rules
    format: json
    schema_ref: freeform
    frequency: on_demand
    criticality: important
    description: Custom validation logic beyond JSON schema (e.g. cross-field rules)
```

### Consumes

```yaml
consumes:
  - name: schema_violation_reports
    format: notification
    source: agents (when input/output fails schema validation)
    frequency: on_event

  - name: new_agent_definitions
    format: markdown
    source: agent_developer
    frequency: on_event
```

### Triggers

```yaml
triggered_by:
  - event_type: schema.validation_failure (recurring)
    urgency: next_session
    action: Investigate if schema is too strict, too lax, or agent is non-compliant

  - event_type: agent.created (new agent with new I/O types)
    urgency: next_session
    action: Define schemas for the new agent's inputs and outputs
```

### Absence Impact

```yaml
absence_impact:
  - scenario: Schemas never updated as system evolves
    consequence: Agents pass unstructured data; downstream validation fails or is skipped
    mitigation: Agents use "freeform" schema_ref — works but loses type safety
```

### Evolution Contribution

```yaml
evolution:
  feeds: data contract quality, system composability
  mechanism: >
    Tighter schemas = fewer runtime failures. Schema evolution is DNA
    evolution — it changes how every cell in the organism communicates.
```

---

## Workflow Designer

### Identity

```yaml
name: workflow_designer
title: Workflow Designer
category: builder
organism_analogy: The vascular surgeon — designs the circulation pathways that connect organs
```

### Contributions

```yaml
contributions:
  - name: workflow_definitions
    format: yaml
    schema_ref: freeform
    frequency: on_demand
    criticality: critical
    description: Pipeline definitions that sequence agents, tools, and conditions

  - name: workflow_templates
    format: yaml
    schema_ref: freeform
    frequency: on_demand
    criticality: enhancing
    description: Reusable workflow fragments for common patterns

  - name: conditional_logic
    format: yaml
    schema_ref: freeform
    frequency: on_demand
    criticality: important
    description: Branching, retry, and fallback rules within workflows
```

### Consumes

```yaml
consumes:
  - name: workflow_execution_logs
    format: ndjson
    source: logs/events/ (workflow.*)
    frequency: per_run

  - name: bottleneck_reports
    format: dashboard
    source: orchestrator
    frequency: weekly
```

### Triggers

```yaml
triggered_by:
  - event_type: workflow.failed (structural failure, not agent failure)
    urgency: next_session
    action: Fix workflow definition bug

  - event_type: agent.created (new agent needs integration into pipelines)
    urgency: next_session
    action: Update workflows to include the new agent at the right stage
```

### Absence Impact

```yaml
absence_impact:
  - scenario: Only default feature_pipeline exists
    consequence: OS can only do one type of work; repo evaluation and release are manual
    mitigation: Existing pipelines work for basic flows; advanced scenarios go unautomated
```

### Evolution Contribution

```yaml
evolution:
  feeds: workflow efficiency, pipeline reliability
  mechanism: >
    Better workflows = more efficient circulation. Workflow redesigns based
    on execution logs teach the orchestrator optimal sequencing.
```

---

## Tool Builder

### Identity

```yaml
name: tool_builder
title: Tool Builder
category: builder
organism_analogy: The muscle fiber creator — builds the deterministic actuators agents use
```

### Contributions

```yaml
contributions:
  - name: programs
    format: file
    schema_ref: freeform
    frequency: on_demand
    criticality: important
    description: Shell scripts, CLI tools in programs/ that agents invoke

  - name: scripts
    format: file
    schema_ref: freeform
    frequency: on_demand
    criticality: important
    description: Python/Node scripts in scripts/ for data processing

  - name: tool_documentation
    format: markdown
    schema_ref: freeform
    frequency: per_tool
    criticality: enhancing
    description: Usage docs, expected input/output, exit codes
```

### Consumes

```yaml
consumes:
  - name: tool_failure_logs
    format: ndjson
    source: agents (when tools error during invocation)
    frequency: on_event

  - name: agent_tool_requests
    format: notification
    source: agent_developer (when new agents need tools that don't exist)
    frequency: on_event
```

### Triggers

```yaml
triggered_by:
  - event_type: tool.failed (recurring)
    urgency: next_session
    action: Fix or replace the broken tool

  - event_type: agent.created (needs tools not yet built)
    urgency: next_session
    action: Build the required tools
```

### Absence Impact

```yaml
absence_impact:
  - scenario: Tools are buggy or missing
    consequence: Agents can't execute; coding agent can't self-test, deploy.sh fails
    mitigation: Agents degrade to doing without the tool (lower quality output)
```

### Evolution Contribution

```yaml
evolution:
  feeds: tool reliability, agent capability
  mechanism: >
    Better tools = stronger muscles. Each tool improvement makes every
    agent that uses it more capable. Tool docs feed into agent context.
```

---

## Integration Engineer

### Identity

```yaml
name: integration_engineer
title: Integration Engineer
category: builder
organism_analogy: The synapse builder — connects the organism to the external world
```

### Contributions

```yaml
contributions:
  - name: external_connectors
    format: file
    schema_ref: freeform
    frequency: on_demand
    criticality: important
    description: Adapters for GitHub, Linear, Slack, AWS, CI/CD systems

  - name: webhook_endpoints
    format: file
    schema_ref: freeform
    frequency: on_demand
    criticality: important
    description: Inbound triggers that let external systems start OS workflows

  - name: api_bridges
    format: file
    schema_ref: freeform
    frequency: on_demand
    criticality: enhancing
    description: Outbound APIs that expose OS state to external dashboards
```

### Consumes

```yaml
consumes:
  - name: connectivity_mode
    format: json
    source: connectivity_manager
    frequency: on_change

  - name: integration_error_logs
    format: ndjson
    source: event_bus (connectivity-related failures)
    frequency: on_event
```

### Triggers

```yaml
triggered_by:
  - event_type: connectivity.online (new system to integrate)
    urgency: next_session
    action: Build connector for the newly available external system

  - event_type: integration.failed
    urgency: next_session
    action: Debug and fix the broken connector
```

### Absence Impact

```yaml
absence_impact:
  - scenario: No external integrations
    consequence: OS is an island — no ticket sync, no deploy, no notifications
    mitigation: OS works fully offline; manual file-based input/output
```

### Evolution Contribution

```yaml
evolution:
  feeds: organism reach, automation surface area
  mechanism: >
    Each integration extends the organism's senses and reach. A Slack
    connector gives it a voice. A GitHub connector gives it hands in the
    remote codebase. A Linear connector gives it a project memory.
```
