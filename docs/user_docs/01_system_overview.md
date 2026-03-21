# Topic 1: System Overview

These diagrams visualize the complete user journey and how technical responsibilities are divided across the Skyforce platform to operate the `morphOS` factory.

## 1.1 The AI Software Factory Loop Overview

This flowchart traces the end-to-end journey from the moment an operator submits a task ("seed") to the final approved promotion. It highlights how the work moves from orchestration to validation and finally into human review.

```mermaid
flowchart TD
    %% Styling
    classDef intake fill:#e0f2fe,stroke:#0284c7,stroke-width:2px;
    classDef morphos fill:#f3e8ff,stroke:#9333ea,stroke-width:2px;
    classDef symphony fill:#dcfce7,stroke:#16a34a,stroke-width:2px;
    classDef harness fill:#ffedd5,stroke:#ea580c,stroke-width:2px;
    classDef centre fill:#fef08a,stroke:#ca8a04,stroke-width:2px;
    classDef data fill:#f3f4f6,stroke:#4b5563,stroke-width:2px,stroke-dasharray: 5 5;

    A([Seed Input: Ticket/PRD/Issue]):::intake --> B{Workflow Selection}:::morphos
    
    subgraph morphOS [morphOS Domain - Specification]
        B -->|Assigns Archetypes & Layouts| C[Create Workspace]:::morphos
    end
    
    subgraph symphony_env [skyforce-symphony - Orchestration]
        C --> D(Interactive Agent Execution Loop):::symphony
        D <-->|Read/Write Run State| FS[(Filesystem Memory)]:::data
    end
    
    subgraph harness_env [skyforce-harness - Objective Validation]
        D -->|Commands| E{Validation Checks}:::harness
        E -->|Failed Check| D
        E -->|Passed Check| F[Emit Evidence & Receipts]:::harness
    end
    
    subgraph centre_env [skyforce-command-centre - The Operator UI]
        F --> G{Human Approval Gate}:::centre
        G -->|Reject / Rework| D
        G -->|Approve| H([Promote to Source / Actioned]):::centre
        
        F -.-> |Update Visible States| I[(Summary Pyramid)]:::data
    end
    
    H --> J[Feedback Loop: Reusable Artifacts for Future Runs]:::intake
```

***

## 1.2 System Architecture & Boundaries

This diagram breaks down the strict responsibility boundaries of the platform. `morphOS` is not a standalone runtime; it dictates the *rules*, while Symphony, Harness, and Core provide the *engine*.

```mermaid
flowchart LR
    %% Styling
    classDef model_node fill:#f3e8ff,stroke:#9333ea,stroke-width:2px;
    classDef orch_node fill:#dcfce7,stroke:#16a34a,stroke-width:2px;
    classDef exec_node fill:#ffedd5,stroke:#ea580c,stroke-width:2px;
    classDef ui_node fill:#fef08a,stroke:#ca8a04,stroke-width:2px;
    classDef core_node fill:#e2e8f0,stroke:#64748b,stroke-width:2px;
    classDef trait fill:#ffffff,stroke:#cbd5e1,stroke-width:1px,stroke-dasharray: 3 3;

    S[skyforce-symphony]:::orch_node
    H[skyforce-harness]:::exec_node
    C[sky-force-command-centre]:::ui_node
    CORE[skyforce-core]:::core_node

    %% Flow
    S <-->|Requests validation & execution| H
    C -->|Triggers & Approves runs| S
    
    subgraph Model [The Operating Model]
        M[morphOS]:::model_node
        M_T["<b>Owns:</b><br>- Workflow Specs<br>- Archetype Definitions<br>- Artifact Schemas<br>- Approval & Escalation Semantics"]:::trait
        M -.- M_T
    end

    subgraph Orchestrator [The Factory Floor Orchestrator]
        S
        S_T["<b>Owns:</b><br>- Workflow Execution<br>- Shift-Work Mode Management<br>- Run Directory Setup<br>- Approval Pauses & Resumes"]:::trait
        S -.- S_T
    end

    subgraph Executor [The Secure Executor]
        H
        H_T["<b>Owns:</b><br>- Bounded Command Execution<br>- Receipts Generation<br>- Objective Artifact Evidence packaging"]:::trait
        H -.- H_T
    end

    subgraph UI [The Operator Human Plane]
        C
        C_T["<b>Owns:</b><br>- Run Visibility & Queues<br>- Summary Pyramid Display<br>- Operator Approvals & Rejections"]:::trait
        C -.- C_T
    end

    subgraph Contracts [Shared System Contracts]
        CORE
        CORE_T["<b>Owns:</b><br>- Shared Native Schemas<br>- CLI Inspection Tooling<br>- Event Contract Enforcement"]:::trait
        CORE -.- CORE_T
    end

    M -.->|Specifies behavior for| S
    CORE -.-> M
    CORE -.-> S
    CORE -.-> H
    CORE -.-> C
```
