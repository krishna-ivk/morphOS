# Topic 4: Workflows & Resource Topologies

## 4.1 Workflow Pack & Registry Hierarchy

Workflows do not float independently. They are versioned and distributed in governed "Packs" loaded into the "Registry." This diagram shows how the runtime discovers the correct execution template.

```mermaid
classDiagram
    direction TB
    class WorkflowRegistry {
        +List packs
        +List templates
        +Index by_tag
        +Index by_trust_label
    }
    
    class WorkflowPack {
        +String pack_id
        +String version
        +String trust_label (core, curated, experimental)
        +List~WorkflowTemplate~ templates
    }
    
    class WorkflowTemplate {
        +String template_id
        +List selection_tags
        +List required_capabilities
        +List execution_steps
    }

    WorkflowRegistry "1" *-- "many" WorkflowPack : Catalogs & Indexes
    WorkflowPack "1" *-- "many" WorkflowTemplate : Bundles Versioned Definitions
```

***

## 4.2 Filesystem Memory Topology

In standard agents, memory is hidden in LLM context windows. In `morphOS`, memory is explicitly dumped to the filesystem so both agents and operators can read it. Here is the canonical run directory structure.

```mermaid
graph TD
    %% Styling
    classDef dir fill:#bae6fd,stroke:#0284c7,stroke-width:2px;
    classDef file fill:#f3f4f6,stroke:#4b5563,stroke-width:2px,stroke-dasharray: 5 5;

    A[Standard Run Directory]:::dir
    
    A --> B[seed/]:::dir
    A --> C[plan/]:::dir
    A --> D[work/]:::dir
    A --> E[artifacts/]:::dir
    A --> F[validation/]:::dir
    A --> G[summaries/]:::dir
    A --> H[approvals/]:::dir

    %% Detailed files
    B -.-> B1(ticket.md / work_order.json):::file
    C -.-> C1(feature_plan.json):::file
    D -.-> D1(agent_scratchpad.txt):::file
    E -.-> E1(build_output.zip):::file
    F -.-> F1(test_results.json):::file
    G -.-> G1(status.txt / summary_short.md):::file
    H -.-> H1(approval_packet.json):::file
```

***

## 4.3 The Summary Pyramid

To allow agents to instantly understand past work without blowing out their context window (and to give human operators quick insight), every run must emit a "compression pyramid."

```mermaid
flowchart BT
    %% Styling
    classDef base fill:#fef08a,stroke:#ca8a04,stroke-width:2px;
    classDef mid1 fill:#fed7aa,stroke:#ea580c,stroke-width:2px;
    classDef mid2 fill:#fbcfe8,stroke:#db2777,stroke-width:2px;
    classDef peak fill:#e0e7ff,stroke:#4f46e5,stroke-width:2px;

    D[Level 4: evidence.json / receipt_id\nMassive Machine-Readable Detail]:::base
    C[Level 3: summary_full.md\nDetailed Operator Breakdown]:::mid1
    B[Level 2: summary_short.md\nQuick Operator Brief]:::mid2
    A[Level 1: status.txt\nOne-Line Readiness Signal]:::peak

    D -->|Summarized via LLM| C
    C -->|Summarized via LLM| B
    B -->|Collapsed into Status| A
```

***

# Topic 5: Actors & Authorities

## 5.1 Agent Archetype Responsibilities

Agents are not monolithic. `morphOS` maps different behaviors and tool permissions to specific named **Archetypes** that correspond to the phases in the 8-Phase Factory Loop.

```mermaid
flowchart LR
    %% Styling
    classDef arch fill:#f3e8ff,stroke:#9333ea,stroke-width:2px;
    classDef phase fill:#ffffff,stroke:#94a3b8,stroke-width:1px;

    Liaison([Operator Liaison]):::arch -->|Clarifies intent| Intake(Intake Phase):::phase
    Planner([Planner]):::arch -->|Generates architecture| Plan(Planning Phase):::phase
    Coder([Coder]):::arch -->|Writes features| Exec(Execution Phase):::phase
    Validator([Validator]):::arch -->|Calculates evidence| Val(Validation Phase):::phase
    Reviewer([Reviewer]):::arch -->|Checks policies| Rev(Review Phase):::phase
    Releaser([Releaser]):::arch -->|Cuts the branch/tag| Promo(Promotion Phase):::phase
```

***

## 5.2 The Durable Authority Boundary

When an agent hits a wall it cannot safely navigate, or when a policy gate is explicitly locked, authority escalates to human layers strictly defined by their scope.

```mermaid
flowchart TD
    %% Styling
    classDef task fill:#f1f5f9,stroke:#64748b,stroke-width:2px;
    classDef admin fill:#dcfce7,stroke:#16a34a,stroke-width:2px;
    classDef super fill:#fee2e2,stroke:#ef4444,stroke-width:2px;

    A(Agent Encountering Block):::task --> B{Scope of Block?}

    %% Workspace Admin
    B -->|Local Policy Failure| C[Workspace Admin]:::admin
    B -->|Risky Workspace Approval| C
    C -->|Approves / Resolves| D(Task Resumes in Workspace):::task
    
    %% Super Admin Escalation
    B -->|Cross-Workspace Exception| E[Super Admin]:::super
    B -->|Global Policy Override| E
    B -->|Unusually High-Risk Promote| E
    
    C -->|Escalates Authority Upward| E
    E -->|Generates Override Packet| D
    E -->|Rejects System-Wide| F(Task Aborted / Blocked):::task
```
