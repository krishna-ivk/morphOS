# Topic 3: Core Data Schemas (The "DNA")

These diagrams illustrate the actual structural JSON contracts defined in `schemas.md` and the MVP documents that flow between phases.

## 3.1 Task Intake & Translation

This Entity Relationship diagram shows how unstructured seed intent breaks down into specific data types to be picked up by the Coding agents.

```mermaid
erDiagram
    SEED_INTENT ||--|| WORK_ORDER : "normalizes into"
    WORK_ORDER ||--|| FEATURE_PLAN : "generates"
    FEATURE_PLAN ||--|{ TASK_RECORD : "splits into"
    
    SEED_INTENT {
        string source "e.g. GitHub Issue, PRD"
        string raw_text
    }
    
    WORK_ORDER {
        string run_id
        string workflow_selection
        string execution_mode
    }
    
    FEATURE_PLAN {
        string project_name
        list features
        list acceptance_criteria
    }
    
    TASK_RECORD {
        string task_id
        string status "pending | in_progress"
        string assigned_agent
        list depends_on
    }
```

***

## 3.2 Runtime Execution Context & Event Bus

This block visualizes the `Event Envelope` system and the central `Run State` which the Orchestrator tracks so that all agents have a source of truth for the workflow.

```mermaid
classDiagram
    class RunState {
        +String run_id
        +String workflow
        +Enum status (running, paused, failed)
        +Enum connectivity_mode (offline, online_read)
        +List~Step~ steps
    }
    
    class EventEnvelope {
        +UUID event_id
        +String event_type (task.completed, agent.health)
        +String source
        +String run_id
        +Object payload
    }
    
    class StepState {
        +String step_id
        +String agent
        +Enum status
        +String output_ref
    }

    RunState "1" *-- "many" StepState : Contains
    EventEnvelope ..> RunState : Mutates via Event Bus
```

***

## 3.3 Execution Receipts & Evidence

When agents invoke tools or run code, `skyforce-harness` safely traps the execution, determines success, and emits standard receipts that the agents can read later.

```mermaid
flowchart LR
    %% Styling
    classDef coreData fill:#e0e7ff,stroke:#4f46e5,stroke-width:2px;
    
    A(Agent Command) -->|Executes in Sandbox| B(skyforce-harness)
    
    B -->|Generates JSON| C[execution_receipt.json]:::coreData
    B -->|Generates JSON| D[task_evidence.json]:::coreData
    B -->|Generates JSON| E[test_results.json]:::coreData

    C --> F((Approval Packet))
    D --> F
    
    E -->|Pass| F
    E -->|Fail| G((Review Rework Trigger))

    style B fill:#ffedd5,stroke:#ea580c,stroke-width:2px;
```

***

## 3.4 The Capability Store & Learning

When a run ends, `morphOS` extracts lessons and saves them into the `capability_store.json` so downstream runs don't make the same mistakes or recreate the same boilerplate.

```mermaid
mindmap
  root((capability_store.json))
    patterns
      id
      description
      code_example
      learned_from_run_id
      use_count
    bug_fixes
      symptom
      root_cause
      fix
      learned_from_run_id
    architecture_lessons
      lesson
      context
      applies_to_schemas
```
