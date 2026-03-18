# Escalation Target Roles — Those Called When the Organism Can't Self-Heal

---

## On-Call Engineer

### Identity

```yaml
name: oncall_engineer
title: On-Call Engineer
category: escalation_target
organism_analogy: The emergency room doctor — activated only when the organism's self-healing fails
```

### Contributions

```yaml
contributions:
  - name: manual_bug_fix
    format: diff
    schema_ref: freeform
    frequency: on_escalation
    criticality: critical
    description: Fix bugs the debugging_agent declared unfixable

  - name: root_cause_analysis
    format: markdown
    schema_ref: freeform
    frequency: on_escalation
    criticality: important
    description: Deep analysis of why the automated fix failed

  - name: fix_verification
    format: approval
    schema_ref: freeform
    frequency: on_escalation
    criticality: critical
    description: Validate that the manual fix resolves the issue without regressions
```

### Consumes

```yaml
consumes:
  - name: unfixable_report
    format: json
    source: debugging_agent
    frequency: on_escalation

  - name: diagnosis
    format: json
    source: debugging_agent
    frequency: on_escalation

  - name: test_results
    format: json
    source: run_tests.sh
    frequency: on_escalation

  - name: full_stack_trace
    format: text
    source: test output
    frequency: on_escalation
```

### Interfaces

```yaml
interfaces:
  - name: code_editor
    type: file_system
    permission: write
    description: Directly edit source code to apply manual fix

  - name: test_runner
    type: cli
    permission: execute
    description: Re-run tests after applying fix

  - name: escalation_queue
    type: notification
    permission: read
    description: Receive escalation alerts with context
```

### Triggers

```yaml
triggered_by:
  - event_type: agent.escalate (source: debugging_agent)
    urgency: immediate
    action: Review unfixable report, apply manual fix, re-run tests

  - event_type: agent.failed (all retries exhausted)
    urgency: immediate
    action: Investigate why agent couldn't complete; fix root cause
```

### Absence Impact

```yaml
absence_impact:
  - scenario: Escalation unanswered
    consequence: Failed task stays blocked; dependent features cannot proceed
    mitigation: Orchestrator skips blocked task if non-critical; queues for next session

  - scenario: Manual fix introduces new bugs
    consequence: Pipeline re-runs and potentially hits more failures
    mitigation: run_tests.sh and policy_engine validate the fix like any other code change
```

### Evolution Contribution

```yaml
evolution:
  feeds: bug_fixes in capability_store
  mechanism: >
    Every manual fix is gold — it's a case the OS couldn't handle alone.
    The learning_agent records the manual fix (symptom + root cause + fix)
    so the debugging_agent can handle similar bugs autonomously next time.
    Over time, fewer escalations reach this role.
```

---

## Architecture Reviewer

### Identity

```yaml
name: architecture_reviewer
title: Architecture Reviewer
category: escalation_target
organism_analogy: The orthopedic specialist — called when the skeleton needs restructuring
```

### Contributions

```yaml
contributions:
  - name: refactoring_plan
    format: markdown
    schema_ref: freeform
    frequency: on_escalation
    criticality: critical
    description: Plan for restructuring code when architecture_agent flags critical issues

  - name: design_decisions
    format: markdown
    schema_ref: freeform
    frequency: on_escalation
    criticality: important
    description: Architectural choices that are too strategic for agents (monolith vs microservice, SQL vs NoSQL)

  - name: tech_debt_prioritization
    format: json
    schema_ref: freeform
    frequency: on_demand
    criticality: enhancing
    description: Which architecture warnings to fix now vs later
```

### Consumes

```yaml
consumes:
  - name: architecture_report
    format: json
    source: architecture_agent
    frequency: on_escalation

  - name: dependency_analysis
    format: json
    source: dependency_scan.sh
    frequency: on_escalation

  - name: codebase_metrics
    format: json
    source: repo_scan.sh
    frequency: on_escalation
```

### Triggers

```yaml
triggered_by:
  - event_type: architecture_report (overall_health: critical)
    urgency: immediate
    action: Review critical findings and create refactoring plan

  - event_type: coding_agent.escalate (reason: "task requires architectural changes")
    urgency: next_session
    action: Make design decision and decompose into coding tasks
```

### Absence Impact

```yaml
absence_impact:
  - scenario: Critical architecture issues ignored
    consequence: Tech debt compounds; future features become harder to build
    mitigation: policy_engine blocks deployment on critical architecture findings

  - scenario: Strategic design decisions deferred
    consequence: Agents make arbitrary choices; inconsistent architecture emerges
    mitigation: architecture_agent enforces existing constraints; learning_agent records patterns
```

### Evolution Contribution

```yaml
evolution:
  feeds: architecture_lessons in capability_store, architecture constraints
  mechanism: >
    Refactoring plans become templates for future restructuring. Design
    decisions become architecture constraints that coding_agent follows
    permanently. The organism's skeleton strengthens after every review.
```

---

## Domain Expert

### Identity

```yaml
name: domain_expert
title: Domain Expert
category: escalation_target
organism_analogy: The specialist consultant — provides knowledge the organism doesn't have in DNA
```

### Contributions

```yaml
contributions:
  - name: domain_knowledge
    format: natural_language
    schema_ref: freeform
    frequency: on_escalation
    criticality: critical
    description: Business rules, industry regulations, or technical specifics agents lack

  - name: requirement_clarification
    format: natural_language
    schema_ref: freeform
    frequency: on_escalation
    criticality: critical
    description: Answers to "does feature X mean behavior A or behavior B?"

  - name: validation_criteria
    format: natural_language
    schema_ref: freeform
    frequency: on_escalation
    criticality: important
    description: How to verify domain-specific correctness beyond unit tests
```

### Consumes

```yaml
consumes:
  - name: feature_plan
    format: json
    source: vision_agent
    frequency: on_escalation

  - name: ambiguity_flags
    format: json
    source: vision_agent (needs_clarification fields)
    frequency: on_escalation

  - name: generated_code
    format: file
    source: coding_agent
    frequency: on_escalation
```

### Triggers

```yaml
triggered_by:
  - event_type: agent.escalate (source: vision_agent, reason: "needs domain clarification")
    urgency: immediate
    action: Provide domain-specific answers to unblockfeature decomposition

  - event_type: agent.escalate (source: coding_agent, reason: "domain logic unclear")
    urgency: next_session
    action: Explain the business rules that code should implement
```

### Absence Impact

```yaml
absence_impact:
  - scenario: Domain questions unanswered
    consequence: Vision_agent makes assumptions; features may not match business reality
    mitigation: OS flags assumptions explicitly; product_owner may partially substitute

  - scenario: No domain validation
    consequence: Code is "technically correct" but doesn't meet real-world business needs
    mitigation: Acceptance criteria partially substitute; but edge cases are missed
```

### Evolution Contribution

```yaml
evolution:
  feeds: domain-specific patterns in capability_store, enhanced vision interpretation
  mechanism: >
    Domain knowledge shared once is stored permanently. If a domain expert
    explains "in finance, amounts must never be floats, always integers in cents,"
    that becomes a coding pattern + a policy rule. The OS absorbs expert
    knowledge and needs less help each time.
```

---

## Approver / Gate Keeper

### Identity

```yaml
name: approver
title: Approver / Gate Keeper
category: escalation_target
organism_analogy: The prefrontal cortex — the conscious decision maker for high-stakes actions
```

### Contributions

```yaml
contributions:
  - name: deployment_approval
    format: approval
    schema_ref: freeform
    frequency: per_release
    criticality: critical
    description: Final human go/no-go for production deployment

  - name: policy_override_approval
    format: approval
    schema_ref: freeform
    frequency: on_demand
    criticality: critical
    description: Approve exceptions to policy rules (with documented justification)

  - name: scope_change_approval
    format: approval
    schema_ref: freeform
    frequency: on_demand
    criticality: important
    description: Approve adding/removing features from the current sprint
```

### Consumes

```yaml
consumes:
  - name: pre_deploy_report
    format: json
    source: orchestrator (aggregated test + security + architecture status)
    frequency: per_release

  - name: policy_override_request
    format: json
    source: policy_engine (when defer action triggers)
    frequency: on_event

  - name: run_summary
    format: markdown
    source: orchestrator
    frequency: per_release
```

### Triggers

```yaml
triggered_by:
  - event_type: workflow.step.started (step_type: deploy)
    urgency: immediate
    action: Review pre-deploy report and approve or reject

  - event_type: policy.violation (action_on_fail: defer, requires_human: true)
    urgency: immediate
    action: Review the blocked action and decide to override or uphold

  - event_type: scope.change_requested
    urgency: next_session
    action: Approve or reject the scope change
```

### Absence Impact

```yaml
absence_impact:
  - scenario: No deployment approver available
    consequence: Code is built and tested but never shipped; queued indefinitely
    mitigation: Auto-deploy policy for non-production environments; require approval only for prod

  - scenario: Policy overrides never granted
    consequence: Legitimate edge cases are permanently blocked
    mitigation: OS documents the override request; policy_author can add exemption rules
```

### Evolution Contribution

```yaml
evolution:
  feeds: approval patterns, policy refinement
  mechanism: >
    Repeated approvals for the same override request indicate the policy is
    too strict — signal to policy_author to add an exemption. Deployment
    approval patterns (always approved when all tests pass + no critical
    findings) teach the OS which conditions allow auto-deployment.
```
