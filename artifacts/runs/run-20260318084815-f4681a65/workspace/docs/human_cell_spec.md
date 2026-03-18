# Human Cell Specification — The Symbiont Template

## Purpose

Just as every agent is grown from `cell_spec.md`, every human role that
interacts with SkyForce is defined from this template. Humans are not
"users" — they are **symbiont cells** in the organism. Each role feeds
the OS something it cannot produce itself, and receives something it
cannot compute alone.

This template ensures that every human role has a clear contract:
what the OS expects from them, and what they get in return.

---

## Required Fields (Per Role)

### 1. Identity

```yaml
name:          # role id, e.g. product_owner
title:         # human-readable title
category:      # primary_user | operator | builder | observer | escalation_target
organism_analogy: # what biological part this role maps to
```

### 2. Contribution (What the Human Gives the OS)

What this role provides that no agent can produce on its own.

```yaml
contributions:
  - name:        # e.g. "product_vision"
    format:      # markdown | yaml | json | natural_language | approval
    schema_ref:  # schema or "freeform"
    frequency:   # per_project | per_sprint | per_run | on_demand | on_escalation
    criticality: # critical | important | enhancing
    description: # what this contribution does for the organism
```

### 3. Consumption (What the Human Gets from the OS)

What the OS produces that this role needs.

```yaml
consumes:
  - name:        # e.g. "architecture_report"
    format:      # json | markdown | dashboard | notification
    source:      # which agent or component produces this
    frequency:   # per_run | daily | on_demand | on_event
```

### 4. Interfaces (How They Touch the OS)

```yaml
interfaces:
  - name:        # e.g. "CLI", "dashboard", "file_edit"
    type:        # cli | web_ui | file_system | api | chat | notification
    permission:  # read | write | approve | configure
    description: # what they do through this interface
```

### 5. Triggers (When the OS Calls Them)

Events that require this role's attention.

```yaml
triggered_by:
  - event_type:  # e.g. "agent.escalate"
    urgency:     # immediate | next_session | weekly
    action:      # what the human should do
```

### 6. Failure Modes (What Happens If This Role Is Absent)

```yaml
absence_impact:
  - scenario:    # e.g. "no vision document provided"
    consequence: # what breaks in the organism
    mitigation:  # fallback behavior or degraded mode
```

### 7. Evolution Contribution

How this role helps the organism get smarter over time.

```yaml
evolution:
  feeds:         # which memory/learning system benefits
  mechanism:     # how their work enters the learning loop
```

---

## Anti-Patterns (What Human Roles Must NOT Do)

1. **No micromanaging agents** — humans set goals and boundaries, agents choose implementation
2. **No bypassing policy** — a human cannot override `core_safety` without changing the policy file
3. **No direct agent manipulation** — humans interact through interfaces, not by editing agent state mid-run
4. **No undocumented contributions** — if a human changes something, it must flow through a defined input
5. **No single-owner dependency** — the organism should degrade gracefully if any single human role is temporarily absent
