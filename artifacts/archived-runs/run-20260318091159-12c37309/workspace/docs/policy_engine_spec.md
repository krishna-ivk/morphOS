# Policy Engine Specification — The Immune System

## Purpose

The policy engine is the **immune system** of SkyForce. It sits between
intent and action. Every operation — agent invocation, tool execution,
file write, network request, deployment — must pass through a policy
check before it is allowed to proceed.

---

## Design Principles

1. **Default deny** — unlisted actions are blocked, not allowed
2. **Fail closed** — if the policy engine crashes, nothing proceeds
3. **Auditable** — every decision is logged with the rule that triggered it
4. **Layered** — policies stack; the most restrictive rule wins
5. **Hot-reloadable** — policy files can be updated without restarting the system

---

## Policy File Format

Policies are defined in `policies/` as YAML files.

```yaml
# policies/core_safety.yaml

name: core_safety
version: 1
priority: 1000  # higher priority = evaluated first
enabled: true

rules:

  - id: require_tests
    description: "Code changes must include tests"
    trigger:
      event_type: task.completed
      agent: coding_agent
    condition:
      output_contains_file: "**/*_test.*"
    action_on_fail: reject
    message: "Coding agent output rejected: no test files included"

  - id: block_secret_in_code
    description: "No secrets in versioned files"
    trigger:
      event_type: task.completed
    condition:
      output_must_not_match:
        - "AKIA[0-9A-Z]{16}"       # AWS access key
        - "sk-[a-zA-Z0-9]{48}"     # OpenAI key
        - "ghp_[a-zA-Z0-9]{36}"    # GitHub PAT
    action_on_fail: reject
    message: "Potential secret detected in agent output"

  - id: deployment_gate
    description: "Deployment requires all tests passing"
    trigger:
      event_type: workflow.step.started
      step_type: deploy
    condition:
      requires_state:
        test_results.overall_result: "pass"
    action_on_fail: block
    message: "Deployment blocked: tests are not all passing"

  - id: network_write_gate
    description: "External write operations require online_write capability"
    trigger:
      tool_permission: network
      tool_action: write
    condition:
      requires_connectivity: online_write
    action_on_fail: defer
    message: "Network write deferred: insufficient connectivity"

  - id: budget_enforcement
    description: "Agent cannot exceed its token budget"
    trigger:
      event_type: agent.health
    condition:
      resource_check:
        tokens_used: "<= max_tokens_per_run"
    action_on_fail: kill
    message: "Agent terminated: token budget exceeded"
```

---

## Threat Model — What "Infections" Look Like

| Threat | Detection Method | Response |
|---|---|---|
| **Malformed input** | Schema validation against `docs/schemas.md` | Reject input, emit `policy.violation` |
| **Secret leakage** | Regex scan on all outputs | Block output, alert |
| **Runaway agent** | Token/time budget exceeded (from health reports) | Kill agent, emit `agent.failed` |
| **Unauthorized file write** | Tool permission check (only `write`-permitted tools) | Block write, emit `policy.violation` |
| **Unsafe deployment** | Pre-deploy checks (tests must pass, no criticals in arch report) | Block deployment |
| **Prompt injection** | Input sanitization (strip control characters, validate structure) | Reject input |
| **Dependency vulnerability** | `dependency_scan.sh` output check | Warn or block depending on severity |
| **Infinite retry loop** | Retry counter per agent per step | Kill after max_retries |

---

## Decision Flow

```
Agent or Tool requests an action
        │
        ▼
┌─────────────────────┐
│  Load applicable     │
│  policy rules        │
│  (sorted by priority)│
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Evaluate conditions │◄─── run_state.json
│  against current     │◄─── test_results.json
│  system state        │◄─── connectivity flags
└─────────┬───────────┘
          │
    ┌─────┴──────┐
    │            │
  PASS         FAIL
    │            │
    ▼            ▼
 Allow       action_on_fail:
 action       ├─ reject  → block + error to agent
              ├─ defer   → queue for later
              ├─ block   → hard stop + alert
              ├─ warn    → allow but log warning
              └─ kill    → terminate the agent
```

---

## Immune Memory

The policy engine maintains a violation log at `logs/policy_violations.ndjson`:

```json
{
  "timestamp": "2026-03-13T01:00:00Z",
  "rule_id": "block_secret_in_code",
  "agent": "coding_agent",
  "run_id": "run-042",
  "action": "reject",
  "details": "Potential AWS key detected in output file services/auth.py"
}
```

The `learning_agent` reads this log to discover recurring violation
patterns and can recommend policy updates (e.g., "coding_agent repeatedly
tries to hardcode DB credentials — add a pre-prompt reminder").

---

## Policy Precedence

When multiple rules apply to the same action:

1. Highest `priority` number wins
2. If equal priority, most restrictive action wins (`kill > block > reject > defer > warn > allow`)
3. Custom policies override defaults but cannot weaken `core_safety` rules

---

## Quarantine Protocol

When an agent is killed by policy:

1. Agent receives a `SIGTERM`-equivalent (stop processing)
2. Partial outputs are moved to `artifacts/quarantine/{run_id}/{agent}/`
3. A `policy.violation` event is emitted
4. The orchestrator marks the step as `failed` with reason `policy_violation`
5. The orchestrator decides whether to retry with a different agent or escalate to human

---

## Required Policy Files

| File | Purpose | Ships with |
|---|---|---|
| `policies/core_safety.yaml` | Secret detection, budget limits, test requirements | Always active |
| `policies/connectivity.yaml` | Network permission gates | Always active |
| `policies/deployment.yaml` | Pre-deploy validation rules | Active in release workflows |
| `policies/custom.yaml` | User-defined project-specific rules | Optional |
