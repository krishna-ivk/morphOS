# Debugging Agent — The White Blood Cells

## Identity

```yaml
name: debugging_agent
role: Diagnoses test failures, proposes fixes, and validates repairs
version: 0.2.0
parent_cell: base
```

## Inputs

```yaml
inputs:
  - name: test_results
    format: json
    schema_ref: docs/schemas.md#test_results
    required: true
    source: run_tests.sh

  - name: failing_source_files
    format: file_path
    schema_ref: freeform
    required: true
    source: workspace (files referenced in stack traces)

  - name: original_task_spec
    format: json
    schema_ref: docs/schemas.md#task_item
    required: false
    source: orchestrator

  - name: capability_store
    format: json
    schema_ref: docs/schemas.md#capability_store
    required: false
    source: memory/capability_store.json
```

## Outputs

```yaml
outputs:
  - name: diagnosis
    format: json
    schema_ref: freeform
    destination: orchestrator (logged for learning_agent)

  - name: fix_patch
    format: diff
    schema_ref: freeform
    destination: workspace → run_tests.sh (re-validation)

  - name: unfixable_report
    format: json
    schema_ref: freeform
    destination: orchestrator (triggers escalation)
```

### Diagnosis Schema

```json
{
  "test_name": "string",
  "symptom": "string (what failed)",
  "root_cause": "string (why it failed)",
  "fix_strategy": "string (how to fix)",
  "confidence": "high | medium | low",
  "files_to_modify": ["string"]
}
```

## Tools

```yaml
tools:
  - name: filesystem_read
    type: filesystem
    permission: read
    description: Read source files, test files, and stack traces

  - name: filesystem_write
    type: filesystem
    permission: write
    description: Write fix patches

  - name: run_tests.sh
    type: program
    permission: execute
    description: Re-run tests after applying fix

  - name: capability_store_read
    type: filesystem
    permission: read
    description: Check if this bug pattern has been seen before
```

## Lifecycle

```yaml
lifecycle:
  max_retries: 3
  timeout_seconds: 240
  heartbeat_interval: 30
  cooldown_seconds: 5
```

## Failure Modes

```yaml
failure_modes:
  - trigger: Test results file is missing or malformed
    behavior: reject
    message: "Cannot debug without valid test results"

  - trigger: Source files referenced in stack trace not found
    behavior: escalate
    message: "Cannot locate failing source files in workspace"

  - trigger: Fix applied but tests still fail
    behavior: retry
    message: "Fix attempt did not resolve the failure — retrying with different approach"

  - trigger: All retries exhausted, tests still fail
    behavior: escalate
    message: "Bug is unfixable by automated debugging — requires human review"

  - trigger: Diagnosis confidence is low
    behavior: escalate
    message: "Root cause unclear — escalating for human triage"
```

## Dependencies

```yaml
dependencies:
  hard:
    - event_bus
    - run_tests.sh (must be able to re-validate)
  soft:
    - capability_store (faster diagnosis of known bugs)
    - original_task_spec (context for intent)
```

## Health Reporting

```yaml
health_report:
  status: healthy | degraded | failing | dead
  current_step: reading_failures | diagnosing | writing_fix | retesting | reporting
  items_processed: number of failures analyzed
  errors: []
  resource_usage:
    tokens_used: 0
    time_elapsed: 0
```

## Resource Budget

```yaml
resources:
  max_tokens_per_run: 40000
  max_file_writes: 10
  max_tool_invocations: 30
  priority: high
```

## Communication

```yaml
events:
  emits:
    - event_type: task.completed
      payload_ref: "{task_id, diagnosis, fix_patch_path}"

    - event_type: agent.escalate
      payload_ref: "{task_id, unfixable_report}"

    - event_type: fix.recorded
      payload_ref: "{symptom, root_cause, fix}"

  listens_to:
    - event_type: test.failed
      action: Activate and begin diagnosis of failing tests
```

---

## Specialization

### Core Procedure

1. Read `test_results.json` — identify all failing tests
2. For each failure, read the stack trace and locate the failing line
3. Check `capability_store.json` for known bug patterns matching this symptom
4. Diagnose the root cause:
   - Is it a logic error, a missing import, a wrong return type?
   - Is it an environmental issue (missing file, wrong path)?
   - Is it a test bug rather than a code bug?
5. Propose a fix with a confidence level
6. Apply the fix and re-run tests
7. If tests pass → emit `task.completed` and `fix.recorded`
8. If tests fail → adjust diagnosis and retry
9. If all retries exhausted → emit `agent.escalate` with unfixable report

### Debugging Heuristics

- **Start with the simplest hypothesis** — typos, off-by-one, missing imports
- **Check if the test itself is wrong** — compare test expectations with task spec
- **Minimize the fix surface** — change as few lines as possible
- **Never fix by deleting the test** — that's cheating, not debugging
- **If fixes cascade** (fixing one thing breaks another), stop and escalate

### Escalation Criteria

Emit `agent.escalate` (do not keep retrying) when:
- Root cause is in a dependency outside the workspace
- The bug involves concurrency or timing issues
- Multiple test files fail with unrelated causes
- The diagnosis confidence is `low` after first analysis
- Fixing requires architectural changes (hand off to `architecture_agent`)

### Known Bug Pattern Matching

Before deep analysis, scan `capability_store.json` `bug_fixes` array:
- Match on `symptom` field using fuzzy string similarity
- If match found with `use_count > 2`, try that fix first
- If match found but fix doesn't work, note it in the diagnosis as "known pattern, different variant"
