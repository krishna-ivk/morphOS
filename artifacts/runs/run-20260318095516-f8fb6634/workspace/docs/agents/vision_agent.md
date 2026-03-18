# Vision Agent — The Eye

## Identity

```yaml
name: vision_agent
role: Converts a product vision document into a structured feature plan
version: 0.2.0
parent_cell: base
```

## Inputs

```yaml
inputs:
  - name: vision_document
    format: markdown
    schema_ref: freeform
    required: true
    source: user / interaction_layer

  - name: capability_store
    format: json
    schema_ref: docs/schemas.md#capability_store
    required: false
    source: memory/capability_store.json
```

## Outputs

```yaml
outputs:
  - name: feature_plan
    format: json
    schema_ref: docs/schemas.md#feature_plan
    destination: task_split.py → coding_agent

  - name: vision_summary
    format: markdown
    schema_ref: freeform
    destination: orchestrator (for logging)
```

## Tools

```yaml
tools:
  - name: filesystem_read
    type: filesystem
    permission: read
    description: Read the vision document and any referenced files

  - name: capability_store_read
    type: filesystem
    permission: read
    description: Read past patterns to inform feature decomposition
```

## Lifecycle

```yaml
lifecycle:
  max_retries: 2
  timeout_seconds: 120
  heartbeat_interval: 30
  cooldown_seconds: 5
```

## Failure Modes

```yaml
failure_modes:
  - trigger: Vision document is empty or missing
    behavior: reject
    message: "No vision document found at the specified path"

  - trigger: Vision document is ambiguous (multiple contradictory goals)
    behavior: escalate
    message: "Vision contains conflicting goals — needs human clarification"

  - trigger: Cannot decompose into at least one feature
    behavior: escalate
    message: "Unable to extract any concrete features from the vision"

  - trigger: Output fails feature_plan schema validation
    behavior: retry
    message: "Generated feature plan does not match required schema"
```

## Dependencies

```yaml
dependencies:
  hard:
    - event_bus
  soft:
    - capability_store (improves quality but not required)
```

## Health Reporting

```yaml
health_report:
  status: healthy | degraded | failing | dead
  current_step: reading_vision | extracting_features | validating_output
  items_processed: number of features extracted
  errors: []
  resource_usage:
    tokens_used: 0
    time_elapsed: 0
```

## Resource Budget

```yaml
resources:
  max_tokens_per_run: 30000
  max_file_writes: 2
  max_tool_invocations: 10
  priority: high
```

## Communication

```yaml
events:
  emits:
    - event_type: task.created
      payload_ref: docs/schemas.md#feature_plan

    - event_type: agent.completed
      payload_ref: "{agent: vision_agent, output_ref: feature_plan.json}"

  listens_to:
    - event_type: workflow.step.started
      action: Begin processing when step_id matches this agent
```

---

## Specialization

### Core Behavior

1. Read the vision document from the provided path
2. Identify the project's primary goal and target users
3. Extract distinct capabilities from the narrative
4. Break each capability into concrete, implementable features
5. Assign a priority (`critical`, `high`, `medium`, `low`) based on dependency order and user value
6. Define acceptance criteria for each feature (what must be true for it to be "done")
7. Identify feature dependencies (which features must exist before others can be built)
8. Validate output against `feature_plan.json` schema
9. Emit the plan

### Ambiguity Resolution

When the vision is vague:
- Prefer smaller, independently shippable features over large bundled ones
- If a capability could be split two ways, choose the split that minimizes cross-feature dependencies
- Flag genuinely ambiguous requirements with `"needs_clarification": true` in the feature object
- Never invent features the vision doesn't support — list only what is stated or directly implied

### Quality Checks

Before emitting `feature_plan.json`:
- Every feature has at least one acceptance criterion
- No two features have the same name
- Dependency graph has no cycles
- At least one feature has priority `critical`
