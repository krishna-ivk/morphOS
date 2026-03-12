# Primary User Roles — Those Who Give Work to the Organism

---

## Solo Developer

### Identity

```yaml
name: solo_developer
title: Solo Developer
category: primary_user
organism_analogy: The single-celled organism host — the body the OS lives inside
```

### Contributions

```yaml
contributions:
  - name: product_vision
    format: markdown
    schema_ref: freeform
    frequency: per_project
    criticality: critical
    description: The genome — describes what the organism should build

  - name: repo_seed
    format: file_path
    schema_ref: freeform
    frequency: per_project
    criticality: critical
    description: Existing codebase for the OS to analyze and extend

  - name: escalation_resolution
    format: natural_language
    schema_ref: freeform
    frequency: on_escalation
    criticality: important
    description: Answers to questions agents couldn't resolve alone

  - name: deployment_approval
    format: approval
    schema_ref: freeform
    frequency: per_run
    criticality: critical
    description: Final go/no-go on deploying to production

  - name: feedback_on_output
    format: natural_language
    schema_ref: freeform
    frequency: per_run
    criticality: enhancing
    description: "Good/bad" signals on code quality that feed the learning loop
```

### Consumes

```yaml
consumes:
  - name: run_progress
    format: dashboard
    source: orchestrator
    frequency: per_run

  - name: completed_code
    format: file
    source: coding_agent
    frequency: per_task

  - name: architecture_report
    format: markdown
    source: architecture_agent
    frequency: on_demand

  - name: escalation_alerts
    format: notification
    source: event_bus (agent.escalate)
    frequency: on_event
```

### Interfaces

```yaml
interfaces:
  - name: cli
    type: cli
    permission: write
    description: Run workflows, inspect state, approve deployments

  - name: file_editor
    type: file_system
    permission: write
    description: Write vision docs, edit policy files, review generated code

  - name: dashboard
    type: web_ui
    permission: read
    description: Monitor pipeline progress and health
```

### Triggers

```yaml
triggered_by:
  - event_type: agent.escalate
    urgency: next_session
    action: Review unfixable bug and provide guidance

  - event_type: policy.violation
    urgency: next_session
    action: Review quarantined output and decide next steps

  - event_type: workflow.completed
    urgency: next_session
    action: Review final output, approve or request changes
```

### Absence Impact

```yaml
absence_impact:
  - scenario: No vision document provided
    consequence: Pipeline cannot start — vision_agent has no input
    mitigation: OS waits indefinitely; cannot generate features from nothing

  - scenario: Escalation ignored for >24h
    consequence: Blocked tasks remain unresolved; dependent features stall
    mitigation: OS skips blocked task and continues with independent features

  - scenario: No deployment approval
    consequence: Code is built and tested but never shipped
    mitigation: OS queues deployment; deploys automatically if auto-deploy policy is enabled
```

### Evolution Contribution

```yaml
evolution:
  feeds: capability_store (via feedback), policy_memory (via policy edits)
  mechanism: >
    Feedback on generated code ("this pattern is good / bad") is stored by the
    learning agent. Policy edits directly shape future immune system behavior.
    Vision documents over time teach the vision agent about this developer's
    preferred feature decomposition style.
```

---

## Product Owner

### Identity

```yaml
name: product_owner
title: Product Owner
category: primary_user
organism_analogy: The geneticist — writes the DNA that determines what the organism builds
```

### Contributions

```yaml
contributions:
  - name: product_vision
    format: markdown
    schema_ref: freeform
    frequency: per_project
    criticality: critical
    description: High-level product description with goals, users, and success criteria

  - name: acceptance_criteria
    format: natural_language
    schema_ref: freeform
    frequency: per_feature
    criticality: critical
    description: Defines "done" for each feature — directly maps to test assertions

  - name: priority_decisions
    format: natural_language
    schema_ref: freeform
    frequency: per_sprint
    criticality: important
    description: Which features matter most — influences task ordering

  - name: ambiguity_resolution
    format: natural_language
    schema_ref: freeform
    frequency: on_escalation
    criticality: critical
    description: Clarifies vision when vision_agent flags "needs_clarification"
```

### Consumes

```yaml
consumes:
  - name: feature_plan
    format: json
    source: vision_agent
    frequency: per_project

  - name: task_completion_status
    format: dashboard
    source: orchestrator
    frequency: per_run

  - name: acceptance_test_results
    format: json
    source: run_tests.sh
    frequency: per_feature
```

### Interfaces

```yaml
interfaces:
  - name: vision_doc_editor
    type: file_system
    permission: write
    description: Author and revise product_vision.md

  - name: feature_review_ui
    type: web_ui
    permission: read
    description: Review how the OS decomposed their vision into features

  - name: chat
    type: chat
    permission: write
    description: Answer clarification questions from vision_agent
```

### Triggers

```yaml
triggered_by:
  - event_type: agent.escalate (source: vision_agent)
    urgency: immediate
    action: Clarify ambiguous requirements

  - event_type: workflow.completed
    urgency: next_session
    action: Validate that delivered features match acceptance criteria
```

### Absence Impact

```yaml
absence_impact:
  - scenario: Vision document is vague or missing acceptance criteria
    consequence: vision_agent extracts weak features; downstream code may not match intent
    mitigation: vision_agent flags ambiguities; pipeline proceeds with best-effort decomposition

  - scenario: Ambiguity escalations go unanswered
    consequence: Features are built on assumptions that may be wrong
    mitigation: OS records assumptions in run_state; product owner can review and correct post-hoc
```

### Evolution Contribution

```yaml
evolution:
  feeds: vision interpretation quality
  mechanism: >
    Each vision→feature_plan→acceptance cycle teaches the vision_agent what
    decomposition style this product owner prefers. Over time, the OS requires
    fewer clarification escalations.
```

---

## Tech Lead

### Identity

```yaml
name: tech_lead
title: Tech Lead
category: primary_user
organism_analogy: The skeletal blueprint architect — defines the structural constraints the organism must obey
```

### Contributions

```yaml
contributions:
  - name: architecture_constraints
    format: markdown
    schema_ref: freeform
    frequency: per_project
    criticality: important
    description: Rules like "use PostgreSQL, not SQLite" or "all services must be stateless"

  - name: tech_stack_decisions
    format: markdown
    schema_ref: freeform
    frequency: per_project
    criticality: important
    description: Language, framework, and dependency choices

  - name: architecture_report_review
    format: approval
    schema_ref: freeform
    frequency: per_run
    criticality: important
    description: Validates architecture_agent findings and decides which to act on

  - name: coding_standards
    format: markdown
    schema_ref: freeform
    frequency: per_project
    criticality: enhancing
    description: Style guides, naming conventions, module structure expectations
```

### Consumes

```yaml
consumes:
  - name: architecture_report
    format: json
    source: architecture_agent
    frequency: per_run

  - name: dependency_warnings
    format: json
    source: dependency_scan.sh
    frequency: per_run

  - name: code_patches
    format: diff
    source: coding_agent
    frequency: per_task
```

### Interfaces

```yaml
interfaces:
  - name: architecture_doc_editor
    type: file_system
    permission: write
    description: Write architecture constraints and tech stack docs

  - name: code_review
    type: web_ui
    permission: read
    description: Review generated code patches

  - name: policy_editor
    type: file_system
    permission: write
    description: Add architecture-related policy rules
```

### Triggers

```yaml
triggered_by:
  - event_type: agent.completed (source: architecture_agent)
    urgency: next_session
    action: Review architecture report findings

  - event_type: policy.violation (category: dependency)
    urgency: next_session
    action: Decide if blocked dependency should be allowed
```

### Absence Impact

```yaml
absence_impact:
  - scenario: No architecture constraints defined
    consequence: coding_agent makes arbitrary tech choices; inconsistent architecture
    mitigation: architecture_agent flags issues post-hoc; learning_agent records conventions

  - scenario: Architecture reports never reviewed
    consequence: Warnings accumulate without action; tech debt grows silently
    mitigation: Critical-severity findings auto-escalate and block deployment
```

### Evolution Contribution

```yaml
evolution:
  feeds: architecture_lessons in capability_store, policy rules
  mechanism: >
    Architecture constraints become policy rules the immune system enforces.
    Reviews of architecture reports teach the learning agent which patterns
    are approved vs rejected for this project's context.
```

---

## Project Manager

### Identity

```yaml
name: project_manager
title: Project Manager
category: primary_user
organism_analogy: The hypothalamus — regulates priority signals and resource allocation across the organism
```

### Contributions

```yaml
contributions:
  - name: priority_overrides
    format: json
    schema_ref: freeform
    frequency: on_demand
    criticality: important
    description: Reorder task priorities when business needs change

  - name: deadline_signals
    format: json
    schema_ref: freeform
    frequency: per_sprint
    criticality: enhancing
    description: Time-box constraints that influence orchestrator scheduling

  - name: scope_decisions
    format: natural_language
    schema_ref: freeform
    frequency: on_demand
    criticality: important
    description: Cut, defer, or expand feature scope based on progress

  - name: escalation_triage
    format: natural_language
    schema_ref: freeform
    frequency: on_escalation
    criticality: important
    description: Routes escalations to the right specialist
```

### Consumes

```yaml
consumes:
  - name: run_state
    format: json
    source: orchestrator
    frequency: per_run

  - name: task_completion_velocity
    format: dashboard
    source: orchestrator
    frequency: daily

  - name: escalation_queue
    format: notification
    source: event_bus (agent.escalate)
    frequency: on_event
```

### Interfaces

```yaml
interfaces:
  - name: project_dashboard
    type: web_ui
    permission: read
    description: Track pipeline progress, velocity, and blockers

  - name: priority_api
    type: api
    permission: write
    description: Adjust task priorities without restarting the pipeline

  - name: notification_channel
    type: notification
    permission: read
    description: Receive escalation and completion alerts
```

### Triggers

```yaml
triggered_by:
  - event_type: agent.escalate
    urgency: immediate
    action: Triage and route to appropriate specialist

  - event_type: workflow.paused
    urgency: immediate
    action: Decide whether to wait, cancel, or reprioritize

  - event_type: workflow.completed
    urgency: next_session
    action: Update project tracking and stakeholders
```

### Absence Impact

```yaml
absence_impact:
  - scenario: No priority guidance
    consequence: Orchestrator uses default ordering (by dependency); may not match business value
    mitigation: Default priority assignment by vision_agent is usually reasonable

  - scenario: Escalations not triaged
    consequence: Specialists don't know when they're needed; tasks remain blocked
    mitigation: OS falls back to round-robin escalation to all available humans
```

### Evolution Contribution

```yaml
evolution:
  feeds: orchestrator scheduling heuristics
  mechanism: >
    Priority overrides and scope decisions teach the orchestrator which feature
    orderings lead to faster completion. Over time, the OS learns to prioritize
    similar to how this PM would.
```
