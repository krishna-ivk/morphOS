# Shared Data Schemas — The DNA

## Purpose

These schemas define the **standardized data formats** that flow between
agents, tools, and workflows. In organism terms, this is the genetic code —
the shared language every cell uses to communicate.

No agent may produce output that violates its declared schema.
No agent may consume input without validating it against the expected schema.

---

## Core Schemas

### 1. Feature Plan (`feature_plan.json`)

Produced by: `vision_agent`
Consumed by: `task_split.py` → `coding_agent`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["project_name", "features"],
  "properties": {
    "project_name": {
      "type": "string",
      "description": "Name of the project being built"
    },
    "features": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["name", "description", "priority", "acceptance_criteria"],
        "properties": {
          "name": {
            "type": "string",
            "description": "Short feature identifier"
          },
          "description": {
            "type": "string",
            "description": "What this feature does"
          },
          "priority": {
            "type": "string",
            "enum": ["critical", "high", "medium", "low"]
          },
          "acceptance_criteria": {
            "type": "array",
            "items": { "type": "string" },
            "description": "Conditions that must be true for the feature to be considered complete"
          },
          "dependencies": {
            "type": "array",
            "items": { "type": "string" },
            "description": "Names of features that must be built first"
          }
        }
      }
    }
  }
}
```

---

### 2. Task List (`tasks.json`)

Produced by: `task_split.py`
Consumed by: `coding_agent` (one task per agent invocation)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["id", "task", "description", "status", "assigned_agent"],
    "properties": {
      "id": {
        "type": "string",
        "description": "Unique task identifier, e.g. TASK-001"
      },
      "task": {
        "type": "string",
        "description": "Short task name"
      },
      "description": {
        "type": "string",
        "description": "Detailed implementation instructions"
      },
      "status": {
        "type": "string",
        "enum": ["pending", "in_progress", "completed", "failed", "blocked"]
      },
      "assigned_agent": {
        "type": "string",
        "description": "Agent ID that will execute this task"
      },
      "feature_ref": {
        "type": "string",
        "description": "Name of the parent feature from feature_plan.json"
      },
      "depends_on": {
        "type": "array",
        "items": { "type": "string" },
        "description": "Task IDs that must complete first"
      }
    }
  }
}
```

---

### 3. Test Results (`test_results.json`)

Produced by: `run_tests.sh`
Consumed by: `debugging_agent`, `orchestrator`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["run_id", "timestamp", "summary", "tests"],
  "properties": {
    "run_id": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "summary": {
      "type": "object",
      "required": ["total", "passed", "failed", "skipped"],
      "properties": {
        "total":   { "type": "integer" },
        "passed":  { "type": "integer" },
        "failed":  { "type": "integer" },
        "skipped": { "type": "integer" }
      }
    },
    "overall_result": {
      "type": "string",
      "enum": ["pass", "fail"]
    },
    "tests": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "result"],
        "properties": {
          "name":     { "type": "string" },
          "result":   { "type": "string", "enum": ["pass", "fail", "skip", "error"] },
          "duration_ms": { "type": "integer" },
          "error_message": { "type": "string" },
          "stack_trace":   { "type": "string" }
        }
      }
    }
  }
}
```

---

### 4. Architecture Report (`architecture_report.json`)

Produced by: `architecture_agent`
Consumed by: `orchestrator`, `learning_agent`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["repo_path", "timestamp", "findings"],
  "properties": {
    "repo_path":  { "type": "string" },
    "timestamp":  { "type": "string", "format": "date-time" },
    "overall_health": {
      "type": "string",
      "enum": ["healthy", "concerns", "critical"]
    },
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["category", "severity", "description"],
        "properties": {
          "category": {
            "type": "string",
            "enum": ["modularity", "scalability", "security", "dependency", "performance"]
          },
          "severity": {
            "type": "string",
            "enum": ["info", "warning", "critical"]
          },
          "description": { "type": "string" },
          "file_path":   { "type": "string" },
          "recommendation": { "type": "string" }
        }
      }
    }
  }
}
```

---

### 5. Run State (`run_state.json`)

Produced by: `orchestrator`
Consumed by: all agents (read-only), `connectivity_manager`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["run_id", "workflow", "status", "steps"],
  "properties": {
    "run_id":    { "type": "string" },
    "workflow":  { "type": "string" },
    "status":    { "type": "string", "enum": ["running", "paused", "completed", "failed"] },
    "started_at": { "type": "string", "format": "date-time" },
    "connectivity_mode": { "type": "string", "enum": ["offline", "online_read", "online_write", "deploy_enabled"] },
    "steps": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["step_id", "status"],
        "properties": {
          "step_id":    { "type": "string" },
          "agent":      { "type": "string" },
          "status":     { "type": "string", "enum": ["pending", "running", "completed", "failed", "skipped", "deferred"] },
          "started_at": { "type": "string", "format": "date-time" },
          "ended_at":   { "type": "string", "format": "date-time" },
          "output_ref": { "type": "string", "description": "Path to step output artifact" },
          "error":      { "type": "string" }
        }
      }
    }
  }
}
```

---

### 6. Event Envelope (Event Bus Messages)

Every event on the bus uses this envelope:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["event_id", "event_type", "source", "timestamp", "payload"],
  "properties": {
    "event_id":   { "type": "string", "format": "uuid" },
    "event_type": { "type": "string", "description": "e.g. task.completed, test.failed, agent.health" },
    "source":     { "type": "string", "description": "Agent or component that emitted the event" },
    "timestamp":  { "type": "string", "format": "date-time" },
    "run_id":     { "type": "string", "description": "Which workflow run this event belongs to" },
    "payload":    { "type": "object", "description": "Event-specific data, validated by event_type schema" }
  }
}
```

---

### 7. Capability Store (`capability_store.json`)

Produced by: `learning_agent`
Consumed by: `coding_agent`, `debugging_agent`, `architecture_agent`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["patterns", "bug_fixes", "architecture_lessons"],
  "properties": {
    "patterns": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "description", "learned_from", "timestamp"],
        "properties": {
          "id":            { "type": "string" },
          "description":   { "type": "string" },
          "code_example":  { "type": "string" },
          "language":      { "type": "string" },
          "tags":          { "type": "array", "items": { "type": "string" } },
          "learned_from":  { "type": "string", "description": "run_id where this was discovered" },
          "timestamp":     { "type": "string", "format": "date-time" },
          "use_count":     { "type": "integer", "default": 0 }
        }
      }
    },
    "bug_fixes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "symptom", "root_cause", "fix", "timestamp"],
        "properties": {
          "id":          { "type": "string" },
          "symptom":     { "type": "string" },
          "root_cause":  { "type": "string" },
          "fix":         { "type": "string" },
          "tags":        { "type": "array", "items": { "type": "string" } },
          "learned_from": { "type": "string" },
          "timestamp":   { "type": "string", "format": "date-time" },
          "use_count":   { "type": "integer", "default": 0 }
        }
      }
    },
    "architecture_lessons": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "lesson", "context", "timestamp"],
        "properties": {
          "id":           { "type": "string" },
          "lesson":       { "type": "string" },
          "context":      { "type": "string" },
          "applies_to":   { "type": "array", "items": { "type": "string" } },
          "learned_from": { "type": "string" },
          "timestamp":    { "type": "string", "format": "date-time" },
          "use_count":    { "type": "integer", "default": 0 }
        }
      }
    }
  }
}
```

---

## Schema Validation Rules

1. **All agents validate inputs** before starting work — reject malformed data immediately
2. **All agents validate outputs** before emitting — never send downstream garbage
3. **Schema versions** must be tracked — breaking changes require a version bump
4. **Unknown fields** are preserved (open schema) — don't discard data you don't understand
5. **Empty arrays are valid** — absence of items is not an error, but absence of required fields is
