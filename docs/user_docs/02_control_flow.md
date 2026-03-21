# Topic 2: Control Flow & Delivery Lifecycle

These diagrams map out the 8-phase factory loop defined in the `morphOS` specification. They focus on transitions and human-intervention controls.

## 2.1 The 8-Phase Factory Loop

This shows the canonical baseline life of a successful run without deep details of failures. It focuses on handoffs between Planning, Execution, and Validation.

```mermaid
flowchart LR
    %% Styling
    classDef intake fill:#e0f2fe,stroke:#0284c7,stroke-width:2px;
    classDef planning fill:#f3e8ff,stroke:#9333ea,stroke-width:2px;
    classDef execution fill:#ffedd5,stroke:#ea580c,stroke-width:2px;
    classDef review fill:#fef08a,stroke:#ca8a04,stroke-width:2px;
    classDef complete fill:#dcfce7,stroke:#16a34a,stroke-width:2px;

    A(Intake):::intake --> B(Planning):::planning
    B --> C(Assignment):::planning
    C --> D(Execution):::execution
    D --> E(Validation):::execution
    E --> F(Review):::review
    F --> G(Promotion):::review
    G --> H(Closeout):::complete
```

***

## 2.2 Factory Control States (State Machine)

This state diagram tracks the high-level `status` of a workflow. Note the fallback `Blocked` and `Aborted` states which can trigger from anywhere if a policy fails or an operator intervenes.

```mermaid
stateDiagram-v2
    direction TB
    [*] --> intake
    intake --> planning : Ticket parsed
    planning --> ready_to_run : Plan accepted
    ready_to_run --> running : Agents Assigned
    
    running --> awaiting_validation : Execution done
    awaiting_validation --> running : Rework Required
    
    awaiting_validation --> awaiting_review : Validated correctly
    awaiting_review --> planning : Review rejected (Replan)
    
    awaiting_review --> ready_for_promotion : Approved
    ready_for_promotion --> promoted : Workspace Merged
    promoted --> closed : Artifacts stored
    closed --> [*]

    %% Exception States
    state "Exception States" as Exceptions {
        blocked
        aborted
    }
    
    running --> blocked : Hit Guardrail
    awaiting_review --> blocked : Needs Admin
    blocked --> aborted : Fatal Error
```

***

## 2.3 Gates & Human Interventions

This zooms in on the explicit control points where operators or strict policies intervene, pausing the autonomous execution.

```mermaid
flowchart TD
    %% Styling
    classDef gate fill:#fee2e2,stroke:#ef4444,stroke-width:2px,stroke-dasharray: 4 4;
    classDef action fill:#dbeafe,stroke:#3b82f6,stroke-width:2px;

    Start --> Plan[Generate Execution Plan]
    Plan --> G1{plan_gate}:::gate
    
    G1 -->|Approve| Tool[Assign Tools to Agents]
    G1 -->|Replan| Plan
    
    Tool --> G2{tool_gate}:::gate
    G2 -->|Authorize| Exec[Run Tasks]
    G2 -->|Reject| Abort([Aborted]):::action
    
    Exec --> Valid[Calculate Evidence]
    Valid --> G3{validation_gate}:::gate
    
    G3 -->|Retry / Rework| Exec
    G3 -->|Pass| Rev[Generate Approval Packet]
    
    Rev --> G4{review_gate}:::gate
    G4 -->|Reject| Exec
    G4 -->|Approve| Promote[Send PR to Source]
    
    Promote --> G5{promotion_gate}:::gate
    G5 -->|Merge| Close([Closeout & Emit Summaries]):::action
    G5 -->|Hold| Pause([Paused by Operator]):::action
```
