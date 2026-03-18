# Cell Specification — The Universal Agent Template

## Purpose

Every agent in SkyForce is grown from this template. A cell is the smallest
self-contained unit of work. It defines what every agent **must** have —
regardless of specialization — just as every biological cell shares DNA,
a membrane, and a metabolic cycle.

Any new agent is created by **copying this template and filling in the
specialization sections**. If a field cannot be answered, the agent is not
ready to operate.

---

## Required Fields (The Genome)

Every agent definition **must** include all of the following sections.

### 1. Identity

```yaml
name:          # unique machine-readable id, e.g. coding_agent
role:          # one-sentence human description
version:       # semver, e.g. 0.1.0
parent_cell:   # "base" for first-generation, or name of agent it was cloned from
```

### 2. Inputs (What Flows In)

Define every input the agent can accept. Each input must specify:

```yaml
inputs:
  - name:        # e.g. "task_spec"
    format:      # json | markdown | plain_text | file_path
    schema_ref:  # path to JSON schema, or "freeform" if unstructured
    required:    # true | false
    source:      # which agent or system component produces this
```

### 3. Outputs (What Flows Out)

Define every output the agent produces. Downstream consumers depend on these.

```yaml
outputs:
  - name:        # e.g. "patch_file"
    format:      # json | diff | markdown | file
    schema_ref:  # path to JSON schema, or "freeform"
    destination: # which agent or system component consumes this
```

### 4. Tools (Organelles)

List every external tool or program the agent is allowed to invoke.

```yaml
tools:
  - name:        # e.g. "run_tests.sh"
    type:        # program | script | api | filesystem
    permission:  # read | write | execute | network
    description: # what the tool does
```

An agent **may not** use tools not listed here. This is the membrane.

### 5. Lifecycle

Every agent follows this state machine:

```
IDLE → ACTIVATED → RUNNING → REPORTING → IDLE
                      ↓
                   FAILING → RETRYING → RUNNING
                      ↓
                   DEAD (escalate to orchestrator)
```

Define these lifecycle parameters:

```yaml
lifecycle:
  max_retries:          # how many times it can retry before dying (default: 3)
  timeout_seconds:      # max wall-clock time per invocation (default: 300)
  heartbeat_interval:   # seconds between health pings (default: 30)
  cooldown_seconds:     # minimum pause between invocations (default: 5)
```

### 6. Failure Modes

Every agent must declare how it can fail and what happens.

```yaml
failure_modes:
  - trigger:     # e.g. "input schema validation fails"
    behavior:    # reject | retry | escalate | degrade
    message:     # human-readable explanation

  - trigger:     # e.g. "tool timeout"
    behavior:    # retry | escalate
    message:     # ...

  - trigger:     # e.g. "output exceeds size limit"
    behavior:    # truncate | escalate
    message:     # ...
```

### 7. Dependencies (Cannot Live Without)

```yaml
dependencies:
  hard:          # agents/components that MUST be running (e.g. event_bus)
  soft:          # agents/components that improve quality but aren't required
```

### 8. Health Reporting (Self-Monitoring)

Every agent emits a health status at `heartbeat_interval`:

```yaml
health_report:
  status:        # healthy | degraded | failing | dead
  current_step:  # what it's doing right now
  items_processed: # count
  errors:        # list of recent errors
  resource_usage:
    tokens_used: # LLM tokens consumed this invocation
    time_elapsed: # seconds
```

### 9. Resource Budget (Metabolism)

```yaml
resources:
  max_tokens_per_run:    # LLM token cap (default: 50000)
  max_file_writes:       # filesystem write cap (default: 20)
  max_tool_invocations:  # tool call cap (default: 50)
  priority:              # low | normal | high | critical
```

### 10. Communication (Synapses)

How this agent sends and receives signals through the event bus.

```yaml
events:
  emits:
    - event_type:  # e.g. "task.completed"
      payload_ref: # schema for the event payload

  listens_to:
    - event_type:  # e.g. "test.failed"
      action:      # what to do when this event arrives
```

---

## Specialization Extension Point

After all required fields, each agent adds a `## Specialization` section
with domain-specific instructions, heuristics, and examples. This is the
part that makes a `coding_agent` different from a `debugging_agent` — but
both share the same cellular structure above.

---

## Anti-Patterns (What a Cell Must NOT Do)

1. **No god-agents** — a single agent must not own the full lifecycle
2. **No implicit tools** — if a tool isn't listed, the agent can't use it
3. **No silent failure** — every failure must emit a health report
4. **No unbounded work** — every run has token, time, and write limits
5. **No direct agent-to-agent calls** — communication goes through the event bus
