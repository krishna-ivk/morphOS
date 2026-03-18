# Learning Agent — The Hippocampus

## Identity

```yaml
name: learning_agent
role: Extracts reusable patterns, fixes, and lessons from completed runs and stores them in long-term memory
version: 0.2.0
parent_cell: base
```

## Inputs

```yaml
inputs:
  - name: completed_run_state
    format: json
    schema_ref: docs/schemas.md#run_state
    required: true
    source: orchestrator

  - name: event_log
    format: ndjson
    schema_ref: docs/schemas.md#event_envelope
    required: true
    source: logs/events/{date}.ndjson

  - name: test_results
    format: json
    schema_ref: docs/schemas.md#test_results
    required: false
    source: run_tests.sh output

  - name: architecture_report
    format: json
    schema_ref: docs/schemas.md#architecture_report
    required: false
    source: architecture_agent output

  - name: existing_capability_store
    format: json
    schema_ref: docs/schemas.md#capability_store
    required: true
    source: memory/capability_store.json
```

## Outputs

```yaml
outputs:
  - name: updated_capability_store
    format: json
    schema_ref: docs/schemas.md#capability_store
    destination: memory/capability_store.json (overwrite)

  - name: learning_summary
    format: markdown
    schema_ref: freeform
    destination: orchestrator (logged)
```

## Tools

```yaml
tools:
  - name: filesystem_read
    type: filesystem
    permission: read
    description: Read event logs, run state, and existing capability store

  - name: filesystem_write
    type: filesystem
    permission: write
    description: Write updated capability store

  - name: capability_store_read
    type: filesystem
    permission: read
    description: Check for duplicates before adding new entries

  - name: capability_store_write
    type: filesystem
    permission: write
    description: Update capability store with new patterns/fixes/lessons
```

## Lifecycle

```yaml
lifecycle:
  max_retries: 2
  timeout_seconds: 120
  heartbeat_interval: 30
  cooldown_seconds: 10
```

## Failure Modes

```yaml
failure_modes:
  - trigger: Run state or event log is missing
    behavior: reject
    message: "Cannot learn without completed run data"

  - trigger: Capability store is corrupted or unreadable
    behavior: escalate
    message: "Long-term memory is corrupted — needs manual repair"

  - trigger: Extracted pattern is duplicate of existing entry
    behavior: degrade
    message: "Pattern already known — incrementing use_count instead"

  - trigger: Capability store exceeds size limit (>1MB)
    behavior: degrade
    message: "Memory is full — pruning least-used entries before adding new ones"
```

## Dependencies

```yaml
dependencies:
  hard:
    - event_bus
    - filesystem (read event logs, write capability store)
  soft:
    - test_results (enriches bug fix extraction)
    - architecture_report (enriches lesson extraction)
```

## Health Reporting

```yaml
health_report:
  status: healthy | degraded | failing | dead
  current_step: reading_run_data | extracting_patterns | extracting_fixes | extracting_lessons | deduplicating | pruning | writing_store
  items_processed: entries extracted
  errors: []
  resource_usage:
    tokens_used: 0
    time_elapsed: 0
```

## Resource Budget

```yaml
resources:
  max_tokens_per_run: 20000
  max_file_writes: 2
  max_tool_invocations: 15
  priority: low
```

## Communication

```yaml
events:
  emits:
    - event_type: pattern.discovered
      payload_ref: docs/schemas.md#capability_store.patterns[item]

    - event_type: fix.recorded
      payload_ref: docs/schemas.md#capability_store.bug_fixes[item]

    - event_type: lesson.recorded
      payload_ref: docs/schemas.md#capability_store.architecture_lessons[item]

  listens_to:
    - event_type: workflow.completed
      action: Begin learning extraction from the completed run

    - event_type: task.completed
      action: Queue task outputs for pattern analysis

    - event_type: test.failed
      action: Queue failure data for potential fix extraction
```

---

## Specialization

### Core Procedure

1. Read the completed `run_state.json` to understand what happened
2. Read the event log for the run — reconstruct the timeline
3. Identify **what went well** (patterns):
   - Code structures that passed tests on first try
   - Architectural decisions that the architecture agent praised
   - Efficient task decompositions
4. Identify **what went wrong and how it was fixed** (bug fixes):
   - Test failures that debugging_agent resolved
   - What the symptom was, what the root cause was, what the fix was
5. Identify **structural lessons** (architecture lessons):
   - Modularity improvements that reduced failure rates
   - Dependency choices that caused or prevented problems
6. Deduplicate against existing capability store entries
7. If duplicates found, increment `use_count` on existing entry
8. If memory is near capacity, prune entries with `use_count == 0` that are older than 30 days
9. Write updated `capability_store.json`
10. Emit events for each new discovery

### Extraction Quality Rules

- **Patterns must be generalizable** — don't store project-specific code as a "pattern"
- **Bug fixes must include the symptom** — a fix without context is useless
- **Lessons must include the context** — "use dependency injection" means nothing without "when building testable services"
- **Confidence threshold** — only store patterns that appeared in 2+ successful runs, or fixes that resolved failures

### Memory Management (Pruning)

The capability store should not grow without bound:

| Condition | Action |
|---|---|
| Entry `use_count == 0` and older than 30 days | Delete |
| Store exceeds 1MB | Prune lowest `use_count` entries until under 800KB |
| Duplicate symptom + fix pair | Merge, keep highest `use_count` |
| Entry contradicts a newer entry | Archive old entry, keep new one |

### What This Agent Does NOT Do

- It does **not** apply fixes (that's `debugging_agent`)
- It does **not** change code (that's `coding_agent`)
- It does **not** decide what to build next (that's the orchestrator)
- It **only** observes completed work and distills knowledge
