# Observer Roles — Those Who Monitor the Organism

---

## QA / Tester

### Identity

```yaml
name: qa_tester
title: QA / Tester
category: observer
organism_analogy: The diagnostic lab — inspects the organism's output for quality defects
```

### Contributions

```yaml
contributions:
  - name: test_strategy_review
    format: markdown
    schema_ref: freeform
    frequency: per_project
    criticality: important
    description: Review and supplement the test coverage agents produce

  - name: acceptance_validation
    format: approval
    schema_ref: freeform
    frequency: per_feature
    criticality: critical
    description: Human validation that features actually meet acceptance criteria

  - name: edge_case_definitions
    format: natural_language
    schema_ref: freeform
    frequency: on_demand
    criticality: enhancing
    description: Edge cases that automated testing missed — adds to test suites

  - name: test_quality_feedback
    format: natural_language
    schema_ref: freeform
    frequency: per_run
    criticality: enhancing
    description: "These tests are too shallow / too brittle / missing integration tests"
```

### Consumes

```yaml
consumes:
  - name: test_results
    format: json
    source: run_tests.sh
    frequency: per_run

  - name: generated_test_files
    format: file
    source: coding_agent
    frequency: per_task

  - name: coverage_report
    format: json
    source: run_tests.sh (with coverage flag)
    frequency: per_run
```

### Interfaces

```yaml
interfaces:
  - name: test_viewer
    type: web_ui
    permission: read
    description: Browse test results, coverage, and failure history

  - name: test_file_editor
    type: file_system
    permission: write
    description: Add manual test cases that agents should include
```

### Triggers

```yaml
triggered_by:
  - event_type: workflow.completed
    urgency: next_session
    action: Review test coverage and validate acceptance criteria

  - event_type: test.passed (but coverage below threshold)
    urgency: next_session
    action: Identify undertested areas and add edge cases
```

### Absence Impact

```yaml
absence_impact:
  - scenario: No human test validation
    consequence: Agent-generated tests may pass but miss real-world edge cases
    mitigation: Architecture agent flags low coverage; policy can enforce coverage floor

  - scenario: No edge case input
    consequence: System only tests happy paths; production bugs likely
    mitigation: Learning agent discovers edge cases from production failures over time
```

### Evolution Contribution

```yaml
evolution:
  feeds: test quality patterns in capability_store
  mechanism: >
    Edge cases and quality feedback teach the coding agent to write better
    tests from the start. Over time, the OS proactively covers the edge
    cases that humans previously had to add manually.
```

---

## Security Auditor

### Identity

```yaml
name: security_auditor
title: Security Auditor
category: observer
organism_analogy: The pathologist — examines the organism for hidden diseases and vulnerabilities
```

### Contributions

```yaml
contributions:
  - name: security_assessment
    format: markdown
    schema_ref: freeform
    frequency: per_release
    criticality: critical
    description: Expert review of the OS's security posture and generated code

  - name: vulnerability_reports
    format: json
    schema_ref: freeform
    frequency: on_demand
    criticality: critical
    description: Identified vulnerabilities with severity and remediation steps

  - name: penetration_test_results
    format: markdown
    schema_ref: freeform
    frequency: per_release
    criticality: important
    description: Active testing of the OS and deployed applications for exploits

  - name: compliance_gap_analysis
    format: markdown
    schema_ref: freeform
    frequency: per_project
    criticality: important
    description: Mapping of current state against regulatory requirements
```

### Consumes

```yaml
consumes:
  - name: policy_violation_log
    format: ndjson
    source: logs/policy_violations.ndjson
    frequency: weekly

  - name: quarantined_outputs
    format: file
    source: artifacts/quarantine/
    frequency: on_event

  - name: dependency_scan_results
    format: json
    source: dependency_scan.sh
    frequency: per_run

  - name: architecture_report
    format: json
    source: architecture_agent (security findings)
    frequency: per_run
```

### Interfaces

```yaml
interfaces:
  - name: audit_dashboard
    type: web_ui
    permission: read
    description: Security-focused view of violations, quarantined items, and vuln scans

  - name: quarantine_viewer
    type: file_system
    permission: read
    description: Inspect quarantined agent outputs for actual threats
```

### Triggers

```yaml
triggered_by:
  - event_type: policy.violation (severity: critical, category: security)
    urgency: immediate
    action: Assess if this is a real security breach

  - event_type: architecture_report (finding.category: security, severity: critical)
    urgency: immediate
    action: Validate finding and recommend immediate action
```

### Absence Impact

```yaml
absence_impact:
  - scenario: No security audit before deployment
    consequence: Unknown vulnerabilities may ship to production
    mitigation: policy_engine blocks deploys with critical security findings; dependency_scan catches known CVEs

  - scenario: Quarantine never reviewed by human
    consequence: Cannot distinguish false positives from real threats
    mitigation: Conservative policy — quarantined items stay blocked permanently
```

### Evolution Contribution

```yaml
evolution:
  feeds: policy rules, secret detection patterns, security_lessons in capability_store
  mechanism: >
    Every audit finding that becomes a policy rule permanently protects the
    organism against that vulnerability class. Penetration test results teach
    the immune system new attack patterns.
```

---

## Compliance Officer

### Identity

```yaml
name: compliance_officer
title: Compliance Officer
category: observer
organism_analogy: The health inspector — ensures the organism meets external regulatory standards
```

### Contributions

```yaml
contributions:
  - name: compliance_requirements
    format: markdown
    schema_ref: freeform
    frequency: per_project
    criticality: critical
    description: Regulatory requirements (GDPR, SOC2, HIPAA) the OS must satisfy

  - name: audit_trail_validation
    format: approval
    schema_ref: freeform
    frequency: per_release
    criticality: critical
    description: Sign-off that event logs and run records meet audit requirements

  - name: data_handling_policies
    format: yaml
    schema_ref: freeform
    frequency: per_project
    criticality: critical
    description: Rules about data retention, PII handling, geographic restrictions
```

### Consumes

```yaml
consumes:
  - name: complete_event_logs
    format: ndjson
    source: logs/events/
    frequency: per_audit

  - name: run_state_history
    format: json
    source: all run_state.json files
    frequency: per_audit

  - name: policy_violation_history
    format: ndjson
    source: logs/policy_violations.ndjson
    frequency: per_audit
```

### Triggers

```yaml
triggered_by:
  - event_type: regulatory_change
    urgency: next_session
    action: Update compliance requirements and data handling policies

  - event_type: audit_scheduled
    urgency: next_session
    action: Validate all logs and records are complete and compliant
```

### Absence Impact

```yaml
absence_impact:
  - scenario: No compliance review
    consequence: Organization may violate regulations unknowingly
    mitigation: Event logging is always on; data is preserved for retroactive audit
```

### Evolution Contribution

```yaml
evolution:
  feeds: data_handling policies, audit trail quality
  mechanism: >
    Compliance requirements become policy rules that are permanently enforced.
    Audit findings improve logging granularity and data retention strategies.
```

---

## Performance Analyst

### Identity

```yaml
name: performance_analyst
title: Performance Analyst
category: observer
organism_analogy: The sports physiologist — measures the organism's efficiency and identifies bottlenecks
```

### Contributions

```yaml
contributions:
  - name: performance_benchmarks
    format: json
    schema_ref: freeform
    frequency: per_project
    criticality: enhancing
    description: Baseline metrics for acceptable agent performance

  - name: cost_optimization_recommendations
    format: markdown
    schema_ref: freeform
    frequency: monthly
    criticality: enhancing
    description: Where token budgets are wasted; which agents are over-resourced

  - name: bottleneck_analysis
    format: markdown
    schema_ref: freeform
    frequency: on_demand
    criticality: important
    description: Which pipeline stages are slowest and why
```

### Consumes

```yaml
consumes:
  - name: agent_health_reports
    format: json
    source: all agents
    frequency: continuous

  - name: run_state_history
    format: json
    source: all completed runs
    frequency: on_demand

  - name: token_usage_logs
    format: json
    source: health_reports.resource_usage
    frequency: per_run
```

### Triggers

```yaml
triggered_by:
  - event_type: agent.health (tokens_used near budget ceiling)
    urgency: next_session
    action: Analyze if budget is too low or agent is inefficient

  - event_type: workflow.completed (duration > 2× historical average)
    urgency: next_session
    action: Identify what caused the slowdown
```

### Absence Impact

```yaml
absence_impact:
  - scenario: No performance monitoring
    consequence: Token costs grow silently; slow pipelines aren't noticed
    mitigation: Budget enforcement kills runaway agents; default budgets are conservative
```

### Evolution Contribution

```yaml
evolution:
  feeds: resource_budgets in cell_spec, orchestrator scheduling
  mechanism: >
    Performance data tunes agent budgets. Bottleneck analysis leads to
    workflow redesigns. Cost data justifies agent splits (one fat agent →
    two lean specialists).
```
