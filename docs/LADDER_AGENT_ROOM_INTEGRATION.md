# Ladder Integration For morphOS Agent Room

Canonical priority note: use [MORPHOS_V0_IMPLEMENTATION_BOARD.md](/Users/shivakrishnayadav/Documents/skyforce/docs/MORPHOS_V0_IMPLEMENTATION_BOARD.md) for the authoritative cross-repo build order. This document describes how `danielmiessler/Ladder` can be integrated into the `morphOS-agent-room` repository and the wider software-factory model without violating current ownership boundaries.

## Purpose

This document answers:

- where `Ladder` fits in the `morphOS-agent-room` stack
- which `Ladder` objects should become first-class room objects
- how those objects should connect to artifacts, tasks, approvals, and exports
- which parts belong in the room versus the downstream software factory
- what a practical `v1` integration path should look like

Read this alongside:

- [README.md](/Users/shivakrishnayadav/Documents/skyforce/README.md)
- [MORPHOS_V0_CORE_STACK.md](/Users/shivakrishnayadav/Documents/skyforce/docs/MORPHOS_V0_CORE_STACK.md)
- [morphos_buildability_plan.md](/Users/shivakrishnayadav/Documents/skyforce/docs/morphos_buildability_plan.md)
- [SOFTWARE_FACTORY_TECHNIQUES_FOR_MORPHOS.md](/Users/shivakrishnayadav/Documents/skyforce/docs/SOFTWARE_FACTORY_TECHNIQUES_FOR_MORPHOS.md)
- `../morphos-agent-room/README.md`
- `../morphos-agent-room/docs/artifact-design-philosophy.md`
- `../morphos-agent-room/docs/shared-task-board.md`

## Executive Summary

`Ladder` is highly compatible with `morphOS-agent-room` when it is used as the
room's structured discovery and validation grammar.

It is not compatible as a second top-level orchestration runtime.

The clean model is:

- `morphOS-agent-room` owns collaborative workspace behavior
- `Ladder` owns the internal research and optimization loop
- the software factory owns downstream execution and promotion of validated work

In practical terms:

- `Sources`, `Ideas`, `Hypotheses`, `Experiments`, `Results`, and `Algorithms`
  become workspace-scoped structured objects
- those objects render through the existing artifact panel patterns
- experiments connect to the shared task board for execution
- validated results and promoted algorithms feed the existing export contract
- speculative ideation stays in the room until it crosses an explicit gate

## Role Separation

### What Ladder Should Be Responsible For

Inside `morphOS-agent-room`, `Ladder` should provide:

- a canonical object model for research and ideation
- explicit transitions from observation to validation
- a link graph between evidence, claims, tests, and outcomes
- a reusable promotion path from repeated results to room playbooks

### What Ladder Should Not Be Responsible For

Inside `morphOS-agent-room`, `Ladder` should not replace:

- LiveView workspace interaction
- multi-agent session management
- message streaming or agent runtime loops
- shared task persistence
- factory export orchestration
- operator approval handling as a whole

That boundary preserves the existing `morphOS` rule:

- `morphOS` defines the organism
- Skyforce runs the organism

And at the room level:

- `agent-room` hosts the collaborative execution surface
- `Ladder` shapes how the room learns

## Architectural Placement

The right architectural placement is:

- user and agents collaborate in a workspace
- workspace state includes conversations, tasks, approvals, and artifacts
- `Ladder` entities live as workspace-scoped structured objects
- the artifact panel visualizes those entities
- the task board operationalizes experiments
- the export connector serializes validated room outputs into factory packets

This means `Ladder` belongs closest to:

- artifact state
- shared knowledge state
- decision state
- experiment tracking

It does not belong closest to:

- low-level agent runtime scheduling
- queueing and concurrency internals
- websocket streaming
- durable job execution outside the room

## Ladder Object Mapping

The six `Ladder` collections map cleanly into room-native objects.

### 1. Sources

Meaning in the room:

- raw inputs that may influence a room's direction

Examples:

- user problem statements
- repo context
- external links
- research papers
- telemetry snapshots
- bug reports
- prior decisions

Suggested object shape:

- `id`
- `workspace_id`
- `title`
- `kind`
- `origin`
- `uri_or_ref`
- `summary`
- `excerpt`
- `relevance`
- `created_by`
- `created_at`

### 2. Ideas

Meaning in the room:

- candidate approaches generated from one or more sources

Suggested object shape:

- `id`
- `workspace_id`
- `title`
- `summary`
- `derived_from_source_ids`
- `expected_upside`
- `novelty`
- `risks`
- `status`
- `created_by`
- `created_at`

### 3. Hypotheses

Meaning in the room:

- testable claims derived from ideas

Suggested object shape:

- `id`
- `workspace_id`
- `idea_id`
- `title`
- `claim`
- `success_metric`
- `failure_metric`
- `measurement_method`
- `status`
- `created_by`
- `created_at`

### 4. Experiments

Meaning in the room:

- concrete test plans created to evaluate hypotheses

Suggested object shape:

- `id`
- `workspace_id`
- `hypothesis_id`
- `title`
- `method`
- `owner`
- `evaluation_plan`
- `task_ids`
- `status`
- `started_at`
- `completed_at`

### 5. Results

Meaning in the room:

- observed findings from completed experiments

Suggested object shape:

- `id`
- `workspace_id`
- `experiment_id`
- `title`
- `outcome`
- `observations`
- `metrics`
- `evidence_refs`
- `decision`
- `confidence`
- `created_by`
- `created_at`

### 6. Algorithms

Meaning in the room:

- promoted reusable methods derived from repeated or high-confidence results

Suggested object shape:

- `id`
- `workspace_id`
- `title`
- `procedure`
- `derived_from_result_ids`
- `preconditions`
- `known_limits`
- `adoption_scope`
- `status`
- `approved_by`
- `approved_at`

## Persistence Model

The canonical `Ladder` graph should be workspace-scoped durable state, not
derived from chat history and not tied to one agent's checkpoint.

Recommended storage rule:

- conversations remain in thread entries
- per-agent private outputs can still use per-session artifacts
- shared `Ladder` entities live in dedicated workspace-scoped tables

This follows the same logic already used by the shared task board design:

- `Ladder` objects have multiple writers
- they need shared visibility
- they must survive refresh and restart
- they should outlive any single agent session

### Suggested `v1` Tables

- `ladder_sources`
- `ladder_ideas`
- `ladder_hypotheses`
- `ladder_experiments`
- `ladder_results`
- `ladder_algorithms`

Each table should include:

- a primary key
- `workspace_id`
- lifecycle timestamps
- `created_by`
- `status`

Link edges may be modeled either through join tables or array references.

For `v1`, simple explicit foreign keys plus relation tables are safer:

- `ladder_idea_sources`
- `ladder_result_evidence_refs`
- `ladder_algorithm_results`

## Artifact Panel Integration

`morphOS-agent-room` already has a strong artifact philosophy:

- backend owns structured state
- frontend renders that state
- the chat column should not be parsed into data objects

The clean UI pattern is one unified `Ladder` artifact surface with six sections:

- `Sources`
- `Ideas`
- `Hypotheses`
- `Experiments`
- `Results`
- `Algorithms`

This can be implemented as:

- one workspace-scoped `ladder` artifact with subsection views

or:

- six coordinated artifact tabs

The first option is better for `v1` because it preserves the relationship
between stages instead of scattering them across unrelated tabs.

### Recommended UI Sections

- `Inbox`
  - newly added sources and raw inputs
- `Incubator`
  - ideas under active discussion
- `Claims`
  - hypotheses waiting for validation
- `Tests`
  - experiments in flight
- `Findings`
  - results with evidence
- `Playbook`
  - promoted algorithms and reusable methods

## Shared Task Board Integration

The task board should remain the execution surface for `Ladder` experiments.

Recommended mapping:

- an approved hypothesis may create an experiment
- an accepted experiment may create one or more tasks
- tasks track the operational work needed to run the experiment
- completed tasks prompt result capture
- repeated confirmed results may be promoted to algorithms

### Linking Rule

Every experiment should keep a durable link to task board objects:

- `experiment.task_ids`
- `tasks.external_ref = "EX-xxxxx"` or equivalent

This gives the room:

- a reasoning object for why work exists
- an execution object for how work is being performed

That is the key complement between `Ladder` and the shared task board.

## Workflow Gates

To prevent speculative room chatter from becoming premature factory output,
`Ladder` transitions should be gated.

### Suggested State Machine

- `Source`
  - `captured`
  - `triaged`
- `Idea`
  - `proposed`
  - `shortlisted`
  - `rejected`
- `Hypothesis`
  - `draft`
  - `ready`
  - `archived`
- `Experiment`
  - `planned`
  - `running`
  - `completed`
  - `aborted`
- `Result`
  - `recorded`
  - `reviewed`
  - `validated`
  - `rejected`
- `Algorithm`
  - `candidate`
  - `approved`
  - `published`
  - `retired`

### Minimum Gate Rules

- an idea cannot become an experiment directly
- every experiment must reference a hypothesis
- every hypothesis must declare a success metric
- every result must attach evidence or observations
- only validated results can be considered for promotion
- only approved algorithms should be exportable as factory guidance

## Approval Model

The room already exports approval packets, so `Ladder` should feed into that
instead of inventing a parallel approval channel.

Recommended approval policy:

- ideas do not require human approval by default
- experiments that are expensive, risky, or irreversible require approval
- algorithm promotion requires either:
  - multiple validated supporting results
  - or explicit human approval
- factory export from `Ladder` should require approval when the output is meant
  to shape downstream execution

## Export Contract

The exporter should not serialize the entire `Ladder` workspace by default.

It should export the validated and decision-ready subset.

### Exportable Objects

- shortlisted or adopted decisions
- reviewed or validated results
- approved algorithms
- supporting evidence references
- short and full summaries for operators

### Suggested Export Additions

Add these files under the current room export layout:

- `artifacts/ladder/result_register.json`
- `artifacts/ladder/algorithm_register.json`
- `memory/ladder_context_index.json`
- `plan/experiment_plan.json`
- `summaries/ladder_summary_short.md`
- `summaries/ladder_summary_full.md`

### Work Order Rule

`seed/work_order.json` should be generated only from:

- approved algorithms
- validated results with clear action implications
- explicitly approved experiments when the factory itself is expected to run the
  next test

Raw sources, loose ideas, and unvalidated hypotheses should stay inside the room.

## Agent Role Design

The room should assign `Ladder` responsibilities by role instead of letting
every agent perform every stage equally.

Suggested role split:

- research agent
  - source capture and relevance tagging
- strategist agent
  - idea formation and clustering
- analyst agent
  - hypothesis drafting and success metrics
- executor agent
  - experiment definition and task creation
- reviewer agent
  - result evaluation and confidence scoring
- architect or librarian agent
  - algorithm promotion and playbook curation

This role specialization should improve:

- signal quality
- less duplicated ideation
- clearer artifacts
- stronger room exports

## Tool Surface

The minimal useful `Ladder` tool set for the room is:

- `add_source`
- `list_sources`
- `propose_idea`
- `shortlist_idea`
- `form_hypothesis`
- `start_experiment`
- `record_result`
- `promote_algorithm`

Each tool should write structured room state, not free-form message text.

### Example Tool Flows

`add_source`

- captures a new source object
- links it to workspace context
- refreshes the Ladder panel

`start_experiment`

- verifies the target hypothesis is `ready`
- creates an experiment object
- optionally creates task-board items
- links those tasks back to the experiment

`record_result`

- attaches metrics and evidence
- marks the experiment complete
- updates downstream promotion eligibility

## `v1` Contract Shapes

The following examples are intentionally small and operational.

They are not final schemas, but they describe the minimum useful shape for
room-native `Ladder` objects.

### Source Example

```json
{
  "id": "SR-00001",
  "workspace_id": "ws_123",
  "title": "Open PRs show repeated rollback issues in deploy pipeline",
  "kind": "repo_observation",
  "origin": "github",
  "uri_or_ref": "https://github.com/org/repo/pull/123",
  "summary": "Recent deploy changes correlate with repeated rollback behavior.",
  "excerpt": "Rollback happened in 3 of the last 5 deploys.",
  "relevance": "high",
  "created_by": "research-agent",
  "created_at": "2026-04-06T12:00:00Z"
}
```

### Idea Example

```json
{
  "id": "ID-00001",
  "workspace_id": "ws_123",
  "title": "Add staged canary verification before global promotion",
  "summary": "Reduce rollback risk by adding a narrow canary gate.",
  "derived_from_source_ids": ["SR-00001"],
  "expected_upside": "Lower failed deployment blast radius.",
  "novelty": "medium",
  "risks": ["Longer deploy latency"],
  "status": "shortlisted",
  "created_by": "strategist-agent",
  "created_at": "2026-04-06T12:10:00Z"
}
```

### Hypothesis Example

```json
{
  "id": "HY-00001",
  "workspace_id": "ws_123",
  "idea_id": "ID-00001",
  "title": "Canary validation reduces rollback rate",
  "claim": "A 5 percent canary phase with health checks will reduce rollback frequency by at least 50 percent.",
  "success_metric": "Rollback rate drops from baseline by >= 50 percent over 10 deploys.",
  "failure_metric": "Rollback rate does not materially improve or latency cost exceeds threshold.",
  "measurement_method": "Compare deploy outcomes and duration across the next 10 releases.",
  "status": "ready",
  "created_by": "analyst-agent",
  "created_at": "2026-04-06T12:20:00Z"
}
```

### Experiment Example

```json
{
  "id": "EX-00001",
  "workspace_id": "ws_123",
  "hypothesis_id": "HY-00001",
  "title": "Run canary gate on staging then low-risk production releases",
  "method": "Introduce a staged canary step and compare rollback outcomes against baseline.",
  "owner": "executor-agent",
  "evaluation_plan": "Collect deploy duration, rollback count, and health-check pass rate.",
  "task_ids": ["task_1", "task_2"],
  "status": "running",
  "started_at": "2026-04-06T13:00:00Z",
  "completed_at": null
}
```

### Result Example

```json
{
  "id": "RE-00001",
  "workspace_id": "ws_123",
  "experiment_id": "EX-00001",
  "title": "Canary gate reduced rollback frequency in initial trial",
  "outcome": "positive",
  "observations": [
    "Rollback count dropped from 3 in 5 deploys to 1 in 6 deploys.",
    "Deploy duration increased by 8 percent."
  ],
  "metrics": {
    "baseline_rollbacks": 3,
    "trial_rollbacks": 1,
    "duration_delta_percent": 8
  },
  "evidence_refs": [
    "artifact://deploy-comparison-2026-04-06",
    "task://task_2"
  ],
  "decision": "validated",
  "confidence": "medium",
  "created_by": "reviewer-agent",
  "created_at": "2026-04-06T18:00:00Z"
}
```

### Algorithm Example

```json
{
  "id": "AL-00001",
  "workspace_id": "ws_123",
  "title": "Canary before broad promotion",
  "procedure": [
    "Deploy to canary slice.",
    "Run health and smoke checks.",
    "Promote only if checks pass and error budget remains healthy."
  ],
  "derived_from_result_ids": ["RE-00001"],
  "preconditions": [
    "Health checks exist.",
    "Rollback automation is available."
  ],
  "known_limits": [
    "Not useful for changes that bypass canary coverage."
  ],
  "adoption_scope": "deployment_workflows",
  "status": "approved",
  "approved_by": "human",
  "approved_at": "2026-04-06T18:20:00Z"
}
```

## Suggested Relational Model

The simplest durable schema for `v1` is a workspace-scoped relational model.

### Core Tables

- `ladder_sources`
- `ladder_ideas`
- `ladder_hypotheses`
- `ladder_experiments`
- `ladder_results`
- `ladder_algorithms`

### Relation Tables

- `ladder_idea_sources`
  - links many sources to one idea
- `ladder_experiment_tasks`
  - links many shared tasks to one experiment
- `ladder_result_evidence_refs`
  - links many evidence references to one result
- `ladder_algorithm_results`
  - links many results to one algorithm

### Minimal Column Set

Every core table should include:

- `id`
- `workspace_id`
- `title`
- `status`
- `created_by`
- `inserted_at`
- `updated_at`

Recommended extra fields:

- `summary` for `sources` and `ideas`
- `claim`, `success_metric`, `failure_metric` for `hypotheses`
- `method`, `evaluation_plan`, `owner` for `experiments`
- `outcome`, `decision`, `confidence`, `metrics` for `results`
- `procedure`, `preconditions`, `known_limits` for `algorithms`

## Suggested Elixir Context Boundaries

If this is built in `morphos-agent-room`, the clean boundary is a dedicated
workspace-scoped context, for example:

- `Murmur.Ladder`
  - public CRUD and transition API
- `Murmur.Ladder.Source`
- `Murmur.Ladder.Idea`
- `Murmur.Ladder.Hypothesis`
- `Murmur.Ladder.Experiment`
- `Murmur.Ladder.Result`
- `Murmur.Ladder.Algorithm`

Recommended API shape:

- `create_source/2`
- `propose_idea/2`
- `shortlist_idea/2`
- `create_hypothesis/2`
- `mark_hypothesis_ready/2`
- `create_experiment/2`
- `link_experiment_tasks/3`
- `record_result/2`
- `validate_result/2`
- `promote_algorithm/2`
- `list_ladder_graph/1`

The API should own transition validation.

Tool actions and LiveView events should call the context instead of mutating
row state ad hoc.

## State Transition Rules

These transition rules should live in the context layer rather than the UI.

### Idea Rules

- `proposed -> shortlisted`
- `proposed -> rejected`
- `shortlisted -> rejected`

### Hypothesis Rules

- `draft -> ready`
- `draft -> archived`
- `ready -> archived`

Constraint:

- a hypothesis may only become `ready` if `success_metric` and
  `failure_metric` are both present

### Experiment Rules

- `planned -> running`
- `planned -> aborted`
- `running -> completed`
- `running -> aborted`

Constraint:

- an experiment may only become `running` if it references a `ready`
  hypothesis

### Result Rules

- `recorded -> reviewed`
- `reviewed -> validated`
- `reviewed -> rejected`

Constraint:

- a result may only become `validated` if at least one evidence ref exists

### Algorithm Rules

- `candidate -> approved`
- `approved -> published`
- `approved -> retired`
- `published -> retired`

Constraint:

- an algorithm may only become `approved` if it references at least one
  validated result or has explicit human override approval

## Artifact Rendering Model

The backend should expose a single derived `LadderGraph` artifact for the UI,
even if the canonical state lives in relational tables.

Suggested read model:

```json
{
  "workspace_id": "ws_123",
  "counts": {
    "sources": 8,
    "ideas": 5,
    "hypotheses": 3,
    "experiments": 2,
    "results": 1,
    "algorithms": 1
  },
  "sections": {
    "inbox": [],
    "incubator": [],
    "claims": [],
    "tests": [],
    "findings": [],
    "playbook": []
  }
}
```

This lets the UI keep following the existing artifact principle:

- backend owns the data model
- frontend renders a stable projection

## Export Contract Details

The room exporter should emit `Ladder` outputs as explicit structured packets.

### `artifacts/ladder/result_register.json`

Suggested shape:

```json
{
  "workspace_id": "ws_123",
  "exported_at": "2026-04-06T18:30:00Z",
  "results": [
    {
      "id": "RE-00001",
      "title": "Canary gate reduced rollback frequency in initial trial",
      "decision": "validated",
      "confidence": "medium",
      "evidence_refs": ["artifact://deploy-comparison-2026-04-06"]
    }
  ]
}
```

### `artifacts/ladder/algorithm_register.json`

Suggested shape:

```json
{
  "workspace_id": "ws_123",
  "exported_at": "2026-04-06T18:30:00Z",
  "algorithms": [
    {
      "id": "AL-00001",
      "title": "Canary before broad promotion",
      "procedure": [
        "Deploy to canary slice.",
        "Run health and smoke checks.",
        "Promote only if checks pass."
      ],
      "derived_from_result_ids": ["RE-00001"]
    }
  ]
}
```

### `memory/ladder_context_index.json`

Suggested shape:

```json
{
  "workspace_id": "ws_123",
  "sources": ["SR-00001"],
  "ideas": ["ID-00001"],
  "hypotheses": ["HY-00001"],
  "experiments": ["EX-00001"],
  "results": ["RE-00001"],
  "algorithms": ["AL-00001"]
}
```

### `plan/experiment_plan.json`

Suggested shape:

```json
{
  "workspace_id": "ws_123",
  "active_experiments": [
    {
      "id": "EX-00001",
      "hypothesis_id": "HY-00001",
      "task_ids": ["task_1", "task_2"],
      "status": "running"
    }
  ]
}
```

## Suggested Build Order

If this moves from documentation to implementation, the safest order is:

1. Add database schema and context APIs.
2. Add read model projection for a single Ladder artifact.
3. Add tool actions that use the context.
4. Add experiment-to-task-board linking.
5. Add export serialization.
6. Add approval policy and promotion rules.

This order keeps the system buildable and avoids UI work getting ahead of the
canonical state model.

## Ecto Schema Drafts

The following drafts are deliberately partial.

They are meant to show shape and ownership, not final syntax.

### `Murmur.Ladder.Source`

```elixir
defmodule Murmur.Ladder.Source do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, :binary_id, autogenerate: true}
  @foreign_key_type :binary_id

  schema "ladder_sources" do
    field :title, :string
    field :kind, :string
    field :origin, :string
    field :uri_or_ref, :string
    field :summary, :string
    field :excerpt, :string
    field :relevance, :string
    field :created_by, :string

    belongs_to :workspace, Murmur.Workspaces.Workspace

    timestamps(type: :utc_datetime_usec)
  end

  def changeset(source, attrs) do
    source
    |> cast(attrs, [
      :workspace_id,
      :title,
      :kind,
      :origin,
      :uri_or_ref,
      :summary,
      :excerpt,
      :relevance,
      :created_by
    ])
    |> validate_required([:workspace_id, :title, :kind, :created_by])
  end
end
```

### `Murmur.Ladder.Idea`

```elixir
defmodule Murmur.Ladder.Idea do
  use Ecto.Schema
  import Ecto.Changeset

  @statuses ~w(proposed shortlisted rejected)

  schema "ladder_ideas" do
    field :title, :string
    field :summary, :string
    field :expected_upside, :string
    field :novelty, :string
    field :risks, {:array, :string}, default: []
    field :status, :string, default: "proposed"
    field :created_by, :string

    belongs_to :workspace, Murmur.Workspaces.Workspace

    timestamps(type: :utc_datetime_usec)
  end

  def changeset(idea, attrs) do
    idea
    |> cast(attrs, [
      :workspace_id,
      :title,
      :summary,
      :expected_upside,
      :novelty,
      :risks,
      :status,
      :created_by
    ])
    |> validate_required([:workspace_id, :title, :status, :created_by])
    |> validate_inclusion(:status, @statuses)
  end
end
```

### `Murmur.Ladder.Hypothesis`

```elixir
defmodule Murmur.Ladder.Hypothesis do
  use Ecto.Schema
  import Ecto.Changeset

  @statuses ~w(draft ready archived)

  schema "ladder_hypotheses" do
    field :title, :string
    field :claim, :string
    field :success_metric, :string
    field :failure_metric, :string
    field :measurement_method, :string
    field :status, :string, default: "draft"
    field :created_by, :string

    belongs_to :workspace, Murmur.Workspaces.Workspace
    belongs_to :idea, Murmur.Ladder.Idea

    timestamps(type: :utc_datetime_usec)
  end

  def changeset(hypothesis, attrs) do
    hypothesis
    |> cast(attrs, [
      :workspace_id,
      :idea_id,
      :title,
      :claim,
      :success_metric,
      :failure_metric,
      :measurement_method,
      :status,
      :created_by
    ])
    |> validate_required([:workspace_id, :idea_id, :title, :claim, :status, :created_by])
    |> validate_inclusion(:status, @statuses)
  end
end
```

### `Murmur.Ladder.Experiment`

```elixir
defmodule Murmur.Ladder.Experiment do
  use Ecto.Schema
  import Ecto.Changeset

  @statuses ~w(planned running completed aborted)

  schema "ladder_experiments" do
    field :title, :string
    field :method, :string
    field :owner, :string
    field :evaluation_plan, :string
    field :status, :string, default: "planned"
    field :started_at, :utc_datetime_usec
    field :completed_at, :utc_datetime_usec

    belongs_to :workspace, Murmur.Workspaces.Workspace
    belongs_to :hypothesis, Murmur.Ladder.Hypothesis

    timestamps(type: :utc_datetime_usec)
  end

  def changeset(experiment, attrs) do
    experiment
    |> cast(attrs, [
      :workspace_id,
      :hypothesis_id,
      :title,
      :method,
      :owner,
      :evaluation_plan,
      :status,
      :started_at,
      :completed_at
    ])
    |> validate_required([
      :workspace_id,
      :hypothesis_id,
      :title,
      :method,
      :owner,
      :status
    ])
    |> validate_inclusion(:status, @statuses)
  end
end
```

### `Murmur.Ladder.Result`

```elixir
defmodule Murmur.Ladder.Result do
  use Ecto.Schema
  import Ecto.Changeset

  @statuses ~w(recorded reviewed validated rejected)

  schema "ladder_results" do
    field :title, :string
    field :outcome, :string
    field :observations, {:array, :string}, default: []
    field :metrics, :map, default: %{}
    field :decision, :string
    field :confidence, :string
    field :status, :string, default: "recorded"
    field :created_by, :string

    belongs_to :workspace, Murmur.Workspaces.Workspace
    belongs_to :experiment, Murmur.Ladder.Experiment

    timestamps(type: :utc_datetime_usec)
  end

  def changeset(result, attrs) do
    result
    |> cast(attrs, [
      :workspace_id,
      :experiment_id,
      :title,
      :outcome,
      :observations,
      :metrics,
      :decision,
      :confidence,
      :status,
      :created_by
    ])
    |> validate_required([
      :workspace_id,
      :experiment_id,
      :title,
      :outcome,
      :status,
      :created_by
    ])
    |> validate_inclusion(:status, @statuses)
  end
end
```

### `Murmur.Ladder.Algorithm`

```elixir
defmodule Murmur.Ladder.Algorithm do
  use Ecto.Schema
  import Ecto.Changeset

  @statuses ~w(candidate approved published retired)

  schema "ladder_algorithms" do
    field :title, :string
    field :procedure, {:array, :string}, default: []
    field :preconditions, {:array, :string}, default: []
    field :known_limits, {:array, :string}, default: []
    field :adoption_scope, :string
    field :status, :string, default: "candidate"
    field :approved_by, :string
    field :approved_at, :utc_datetime_usec

    belongs_to :workspace, Murmur.Workspaces.Workspace

    timestamps(type: :utc_datetime_usec)
  end

  def changeset(algorithm, attrs) do
    algorithm
    |> cast(attrs, [
      :workspace_id,
      :title,
      :procedure,
      :preconditions,
      :known_limits,
      :adoption_scope,
      :status,
      :approved_by,
      :approved_at
    ])
    |> validate_required([:workspace_id, :title, :status])
    |> validate_inclusion(:status, @statuses)
  end
end
```

## Migration Notes

For `v1`, keep migrations explicit and boring.

Recommended choices:

- use one table per Ladder entity family
- use binary IDs to align with existing Murmur workspace/task patterns
- index `workspace_id` on every table
- add composite indexes for common list views

Suggested indexes:

- `ladder_ideas(workspace_id, status)`
- `ladder_hypotheses(workspace_id, status)`
- `ladder_experiments(workspace_id, status)`
- `ladder_results(workspace_id, status)`
- `ladder_algorithms(workspace_id, status)`

If relation tables are added, index both directions:

- `ladder_idea_sources(idea_id)`
- `ladder_idea_sources(source_id)`
- `ladder_experiment_tasks(experiment_id)`
- `ladder_experiment_tasks(task_id)`

## LiveView Integration Notes

The preferred LiveView shape is:

- relational state remains canonical
- context layer assembles a workspace Ladder projection
- the UI subscribes to update events and re-renders the projection

### Suggested Screen Additions

Add one `Ladder` panel inside the existing artifact/data area with:

- stage summary badges
- filter by status
- detail drawer for the selected object
- actions appropriate to the current state

Useful interactions:

- create source from chat selection or manual input
- promote idea to hypothesis
- start experiment from hypothesis
- view linked tasks for an experiment
- record result from an experiment detail view
- promote algorithm from a validated result

### Suggested LiveView Event Names

- `"ladder:create_source"`
- `"ladder:propose_idea"`
- `"ladder:shortlist_idea"`
- `"ladder:create_hypothesis"`
- `"ladder:mark_hypothesis_ready"`
- `"ladder:start_experiment"`
- `"ladder:record_result"`
- `"ladder:validate_result"`
- `"ladder:promote_algorithm"`
- `"ladder:select_object"`

These events should stay thin:

- validate incoming params
- call `Murmur.Ladder`
- refresh the Ladder read model
- push minimal success/error feedback

### PubSub Pattern

The room already uses PubSub for live collaboration.

The Ladder layer should reuse that shape:

- write through context
- broadcast workspace-scoped update event
- LiveView refreshes Ladder projection

Suggested topic:

- `"workspace:#{workspace_id}:ladder"`

Suggested event payload:

```elixir
%{
  workspace_id: workspace_id,
  object_type: :experiment,
  object_id: experiment.id,
  event: :updated
}
```

This keeps the UI reactive without making artifacts the source of truth.

## Tool Action Contracts

If Ladder tools are exposed to agents, each tool should call the same context
layer the UI uses.

### `add_source`

Input:

- `title`
- `kind`
- `origin`
- `uri_or_ref`
- `summary`

Output:

- created source object
- short natural-language confirmation

### `propose_idea`

Input:

- `title`
- `summary`
- `source_ids`
- `expected_upside`

Output:

- created idea object

### `form_hypothesis`

Input:

- `idea_id`
- `title`
- `claim`
- `success_metric`
- `failure_metric`
- `measurement_method`

Output:

- created hypothesis object

### `start_experiment`

Input:

- `hypothesis_id`
- `title`
- `method`
- `evaluation_plan`
- `owner`
- optional `create_tasks`

Output:

- experiment object
- optionally created task IDs

### `record_result`

Input:

- `experiment_id`
- `title`
- `outcome`
- `observations`
- `metrics`
- `evidence_refs`

Output:

- result object

### `promote_algorithm`

Input:

- `result_ids`
- `title`
- `procedure`
- `preconditions`
- `known_limits`

Output:

- candidate algorithm object

## End-To-End Event Flow

The most important `v1` event chain is:

1. A user or agent adds a source.
2. Another agent proposes an idea linked to that source.
3. The room forms a hypothesis with explicit metrics.
4. Starting the experiment creates an experiment object and, when needed,
   shared tasks.
5. Task completion triggers or invites result recording.
6. Result validation makes the output eligible for promotion.
7. Algorithm approval makes it eligible for export into factory-facing packets.

That end-to-end chain is the real value of integrating Ladder into the room.

## Example Workspace Sequence

Example sequence for one room:

1. Research agent captures a source from a GitHub issue and a deployment graph.
2. Strategist agent creates two ideas from those sources.
3. Analyst agent marks one hypothesis `ready` after adding measurable success
   criteria.
4. Executor agent starts an experiment and creates two shared tasks.
5. Human and agents watch task completion on the board.
6. Reviewer agent records a result with linked evidence.
7. Human approves a promoted algorithm.
8. Exporter writes the algorithm register and updates the work order.

This gives the room a usable progression from conversation to validated factory
input without collapsing everything into either chat or tasks alone.

## Repo-Specific Placement In `morphos-agent-room`

The current umbrella structure already suggests the clean placement for a
`Ladder` subsystem.

### Existing Repo Surfaces

Relevant existing locations:

- `apps/jido_murmur/lib/jido_murmur/workspaces.ex`
  - workspace and agent-session lifecycle
- `apps/jido_tasks/lib/jido_tasks/tasks.ex`
  - shared task board domain logic
- `apps/jido_artifacts/lib/jido_artifacts/artifact_plugin.ex`
  - artifact signal plumbing
- `apps/murmur_demo/lib/murmur/decisions.ex`
  - durable room decisions
- `apps/murmur_demo/lib/murmur/factory_exports.ex`
  - room export assembly
- `apps/murmur_demo/lib/murmur_web/live/workspace_live.ex`
  - main collaborative room LiveView
- `apps/murmur_demo/lib/murmur_web/components/artifacts/*.ex`
  - artifact renderers
- `connectors/morphos_factory/export_room.py`
  - file-oriented export normalization for the factory

That means `Ladder` does not need a new top-level app immediately.

The most practical `v1` is:

- canonical domain state in `apps/murmur_demo/lib/murmur/ladder/`
- DB migrations in `apps/murmur_demo/priv/repo/migrations/`
- artifact renderer in `apps/murmur_demo/lib/murmur_web/components/artifacts/`
- LiveView event handling in `apps/murmur_demo/lib/murmur_web/live/workspace_live.ex`
- task linkage through `apps/jido_tasks/`
- export augmentation in `apps/murmur_demo/lib/murmur/factory_exports.ex`

### Suggested File Layout

Suggested `v1` additions:

- `apps/murmur_demo/lib/murmur/ladder.ex`
- `apps/murmur_demo/lib/murmur/ladder/source.ex`
- `apps/murmur_demo/lib/murmur/ladder/idea.ex`
- `apps/murmur_demo/lib/murmur/ladder/hypothesis.ex`
- `apps/murmur_demo/lib/murmur/ladder/experiment.ex`
- `apps/murmur_demo/lib/murmur/ladder/result.ex`
- `apps/murmur_demo/lib/murmur/ladder/algorithm.ex`
- `apps/murmur_demo/lib/murmur/ladder/projection.ex`
- `apps/murmur_demo/lib/murmur_web/components/artifacts/ladder_graph.ex`
- `apps/murmur_demo/priv/repo/migrations/*_create_ladder_tables.exs`
- optional `apps/murmur_demo/test/murmur/ladder_test.exs`
- optional `apps/murmur_demo/test/murmur_web/live/workspace_live_ladder_test.exs`

### Why `murmur_demo` Is The Right First Home

The current repo shape shows that `murmur_demo` already hosts:

- workspace-specific product behavior
- room decisions
- export logic
- the main operator UI

By contrast:

- `jido_murmur` is reusable runtime infrastructure
- `jido_tasks` is reusable task-board infrastructure
- `jido_artifacts` is reusable artifact plumbing

So `Ladder` belongs first in `murmur_demo` as product/domain behavior.

If it later proves reusable across multiple Murmur-based products, it can be
promoted into its own umbrella app after the contracts stabilize.

## Package-by-Package Integration Plan

### `apps/jido_murmur`

Use this package unchanged at first except for PubSub/topic convenience if
needed.

Possible light additions:

- helper topic function for workspace Ladder updates
- no Ladder business logic here

Avoid:

- putting Ladder persistence or transition rules in `jido_murmur`

### `apps/jido_tasks`

This remains the shared execution board for experiment work.

Recommended integration:

- add optional metadata or foreign-ref support if the task schema does not
  already expose a good link field
- keep experiment-to-task linking one-directional and explicit

If the existing task schema is rigid, a join table in `murmur_demo` is safer
than forcing Ladder-specific semantics into the reusable task package too early.

### `apps/jido_artifacts`

Use the existing artifact/plugin pipeline for display-oriented projections, not
as the canonical persistence layer.

Recommended role:

- emit or refresh a `ladder_graph` artifact projection for the UI
- do not persist core Ladder state only through artifact plugin state

This is consistent with the room's artifact philosophy and avoids confusing
artifact projection with workspace truth.

### `apps/murmur_demo/lib/murmur`

This should become the home of the Ladder domain context.

Recommended modules:

- `Murmur.Ladder`
  - public domain API
- `Murmur.Ladder.Projection`
  - read model assembly for the artifact panel
- `Murmur.Ladder.*`
  - Ecto schemas

This also keeps `Murmur.Decisions` and `Murmur.FactoryExports` as adjacent
domain modules, which is a strong local fit.

### `apps/murmur_demo/lib/murmur_web/live/workspace_live.ex`

This file is the right place for:

- assigning Ladder projection state on mount
- subscribing to Ladder PubSub updates
- handling Ladder create/promote/record events
- wiring selected Ladder objects into the data panel

Recommended new assigns:

- `:ladder_graph`
- `:active_ladder_object`
- `:ladder_filters`
- `:ladder_form`

Recommended mount additions:

- load `Murmur.Ladder.list_ladder_graph(workspace_id)`
- subscribe to workspace Ladder topic when connected

Recommended handle_info addition:

- on Ladder update, refresh the Ladder projection assign

### `apps/murmur_demo/lib/murmur_web/components/artifacts`

This directory should get a new renderer:

- `ladder_graph.ex`

Its responsibilities should be:

- stage badges
- section lists
- compact counts
- selected-object detail rendering
- action affordances passed back to LiveView events

Keep it presentation-focused.

Do not move transition rules or mutation logic into the component.

### `apps/murmur_demo/lib/murmur/factory_exports.ex`

This is the cleanest place to extend export output for Ladder.

Recommended additions:

- collect validated results for the workspace
- collect approved algorithms for the workspace
- write Ladder register files into the existing export tree
- add Ladder artifact paths into `export_manifest.json`
- optionally enrich `run_memory_index.json` with Ladder references

Recommended approach:

- keep current export behavior working when no Ladder data exists
- treat Ladder export files as additive
- avoid making export success depend on Ladder presence in `v1`

### `connectors/morphos_factory/export_room.py`

This connector already normalizes room data into a filesystem handoff.

If the Elixir-side exporter writes Ladder files directly, the Python connector
may need little or no change for `v1`.

If cross-language parity matters, extend the connector contract to recognize:

- `artifacts/ladder/result_register.json`
- `artifacts/ladder/algorithm_register.json`
- `memory/ladder_context_index.json`
- `plan/experiment_plan.json`

The connector should still stay normalization-focused.

It should not re-derive Ladder semantics from chat transcripts.

## Testing Strategy In The Real Repo

The current repo already has good test seams, so Ladder should follow them.

### Domain Tests

Add tests near:

- `apps/murmur_demo/test/murmur/`

Recommended files:

- `ladder_test.exs`
- `ladder_projection_test.exs`
- `factory_exports_ladder_test.exs`

Cover:

- transition validation
- evidence requirements
- algorithm promotion eligibility
- export payload inclusion

### LiveView Tests

Add tests near:

- `apps/murmur_demo/test/murmur_web/live/`

Recommended files:

- `workspace_live_ladder_test.exs`
- `workspace_live_ladder_projection_test.exs`

Cover:

- Ladder panel rendering
- create/promote flows
- PubSub refresh behavior
- experiment-to-task visibility

### Existing Test Alignment

This repo already has tests for:

- artifact persistence
- workspace reconnect behavior
- task board behavior
- factory export behavior

Ladder should reuse those seams instead of inventing a separate testing style.

## Recommended First PR Slice

The best first implementation slice in the real repo is narrow:

1. Add Ladder schemas and migrations in `murmur_demo`.
2. Add `Murmur.Ladder` with source, idea, and hypothesis support only.
3. Add a basic Ladder projection and renderer.
4. Load that projection in `WorkspaceLive`.
5. Do not implement experiments, export, or algorithm promotion yet.

Why this slice:

- it proves the core state model
- it avoids premature task/export coupling
- it gives immediate UI value
- it keeps the first PR reviewable

## Recommended Second PR Slice

After the first slice lands:

1. Add experiments and experiment-task linking.
2. Reuse the shared task board for execution.
3. Add result recording and validation.

This is the point where Ladder becomes operational rather than just
organizational.

## Recommended Third PR Slice

Then:

1. Add algorithm promotion.
2. Extend `Murmur.FactoryExports`.
3. Add Ladder-aware export files and tests.

This keeps the export contract behind already-stable room semantics.

## Implementation Checklist

This checklist is meant to be executed in order.

### Milestone 1: Core Ladder Domain

Goal:

- create durable workspace-scoped Ladder state without task or export coupling

Tasks:

- add migrations for `ladder_sources`, `ladder_ideas`, and `ladder_hypotheses`
- add Ecto schemas in `apps/murmur_demo/lib/murmur/ladder/`
- add `Murmur.Ladder` context with create/list/transition functions
- add unit tests for changesets and transition rules
- add `Murmur.Ladder.Projection` to build a simple workspace read model

Acceptance criteria:

- a workspace can create and list sources, ideas, and hypotheses
- hypotheses cannot become `ready` without metrics
- projection returns stable sectioned data for the UI

### Milestone 2: Ladder UI Surface

Goal:

- expose Ladder state clearly inside the room

Tasks:

- add `ladder_graph.ex` artifact renderer
- load Ladder projection in `WorkspaceLive.mount/3`
- subscribe to Ladder workspace PubSub topic
- add basic create/select LiveView events
- add LiveView tests for rendering and refresh behavior

Acceptance criteria:

- users can view Ladder sections inside the room
- Ladder objects update live without reload
- UI does not parse transcript text to build Ladder state

### Milestone 3: Experiment Execution Bridge

Goal:

- connect hypotheses to real operational work

Tasks:

- add `ladder_experiments` migration and schema
- add experiment transition rules in `Murmur.Ladder`
- add experiment-to-task relation table or metadata linking
- integrate `start_experiment` with `JidoTasks.Tasks`
- add tests for experiment creation and task linkage

Acceptance criteria:

- only `ready` hypotheses can spawn experiments
- experiments can create and track shared tasks
- the room can navigate from experiment to task and back

### Milestone 4: Results And Promotion

Goal:

- make the room capable of validated learning, not only structured planning

Tasks:

- add `ladder_results` and `ladder_algorithms` migrations and schemas
- add result validation rules and evidence requirements
- add algorithm promotion rules and approval hooks
- add UI flows for recording results and promoting algorithms
- add domain tests for eligibility and rejection paths

Acceptance criteria:

- results require evidence to become `validated`
- algorithms cannot be approved without validated support or explicit override
- validated findings are visible in the Ladder panel

### Milestone 5: Factory Export Integration

Goal:

- hand only validated room outputs into the software factory

Tasks:

- extend `Murmur.FactoryExports` to include Ladder registers
- add Ladder paths to export manifest
- enrich summary files with Ladder output when present
- add export tests for Ladder-aware packets
- optionally extend Python connector validation if needed

Acceptance criteria:

- exports still work when no Ladder data exists
- exports include validated results and approved algorithms when present
- speculative objects do not appear in work-order payloads by default

## Definition Of Done

The Ladder integration should be considered complete for `v1` only when all of
the following are true:

- workspace-scoped Ladder objects persist across refresh and restart
- Ladder state is editable by both humans and agents through supported flows
- task board linkage works for experiments
- result validation is evidence-backed
- export files include only the intended Ladder subset
- the UI can inspect the discovery chain without transcript parsing
- automated tests cover domain transitions, UI rendering, and export output

## Open Questions

These questions should be answered before or during implementation.

### 1. Shared Task Link Shape

Question:

- should experiment-to-task linkage live as a dedicated relation table or as
  task metadata?

Lean recommendation:

- start with a relation table if task schema ownership is unclear

### 2. Artifact Projection Ownership

Question:

- should Ladder appear as a first-class artifact type or as a specialized panel
  outside artifact tabs?

Lean recommendation:

- keep it as an artifact-backed projection first because it fits the current UI
  architecture

### 3. Human Approval Boundary

Question:

- which exact transitions require human approval in `v1`?

Lean recommendation:

- algorithm approval and export-to-factory promotion should require human review
  first

### 4. Connector Parity

Question:

- should the Python connector understand Ladder files explicitly in `v1`, or is
  Elixir-side export enough?

Lean recommendation:

- make Elixir export authoritative first, then add Python parity only if the
  connector is still part of the real operational path

### 5. Reusability Boundary

Question:

- should Ladder stay in `murmur_demo` or be promoted into its own umbrella app?

Lean recommendation:

- keep it in `murmur_demo` until the domain stabilizes across at least one full
  export cycle

## Risks And Failure Modes

The main risks are architectural, not algorithmic.

### Risk 1: Duplicate State Machines

Failure mode:

- Ladder transitions, task statuses, and export states drift apart

Mitigation:

- make `Murmur.Ladder` the canonical owner of Ladder transitions
- keep task board status separate but linked
- derive export eligibility from canonical Ladder state

### Risk 2: UI Becomes The Source Of Truth

Failure mode:

- LiveView assigns or artifact projections begin owning state changes

Mitigation:

- keep writes in context functions only
- make renderers projection-only

### Risk 3: Overfitting To One Agent Type

Failure mode:

- the Ladder flow becomes shaped around one profile instead of a workspace-wide
  model

Mitigation:

- keep all core entities workspace-scoped
- attribute authorship but avoid session-owned persistence

### Risk 4: Premature Export Of Speculative Work

Failure mode:

- ideas or unvalidated hypotheses leak into work-order payloads

Mitigation:

- enforce validation and approval gates inside exporter selection logic

### Risk 5: Too Much Complexity In The First Slice

Failure mode:

- first PR tries to ship schemas, UI, tasks, results, and export all at once

Mitigation:

- keep the first PR limited to sources, ideas, hypotheses, and projection

## Recommended Near-Term Decision

If the goal is to begin implementation soon, the next decision should be:

- approve `murmur_demo` as the `v1` home of the Ladder domain
- approve relational persistence over artifact-only persistence
- approve a first PR limited to source, idea, and hypothesis support

Once those three points are agreed, implementation can start with very little
remaining ambiguity.

## Architecture Decision Matrix

This matrix summarizes the most important design choices in one place.

| Decision Area | Recommended Choice | Why | Rejected Alternative | Rejection Reason |
|---|---|---|---|---|
| Canonical Ladder persistence | Workspace-scoped relational tables in `murmur_demo` | Shared, durable, queryable, and not tied to one agent session | Artifact-only persistence | Confuses projection with truth and weakens shared ownership |
| First implementation home | `apps/murmur_demo/lib/murmur/ladder/` | Fits current product/domain layer and avoids premature package extraction | New umbrella app immediately | Too much abstraction before domain stabilizes |
| UI surface | One unified `Ladder` artifact projection | Preserves cross-stage relationships and fits current artifact architecture | Six unrelated tabs or a transcript-derived view | Scatters context or makes UI reconstruct state |
| Experiment execution | Link experiments to `jido_tasks` shared tasks | Reuses existing execution surface and task UI | Build a second execution board inside Ladder | Duplicates workflow state and operator burden |
| Export strategy | Additive extension of `Murmur.FactoryExports` | Preserves current export path and keeps Ladder optional in `v1` | New export subsystem just for Ladder | Unnecessary duplication and rollout risk |
| Approval boundary | Require human review for algorithm approval and factory promotion | Matches governance needs while keeping ideation fast | Human approval for every Ladder transition | Too heavy for room flow |
| First PR scope | Sources, ideas, hypotheses, projection | Proves shared state and UI value with small risk | Full end-to-end Ladder in one PR | Too broad to review or stabilize safely |

## Object Lifecycle Walkthrough

This section describes the intended lifecycle of each Ladder object in the real
room.

### Source Lifecycle

1. Created by human or agent.
2. Stored durably under the workspace.
3. Appears in the `Inbox` section of the Ladder projection.
4. May be linked to one or more ideas.
5. Remains available as context even if not used immediately.

Expected mutations:

- minor metadata edits
- relevance updates
- source-to-idea linkage

### Idea Lifecycle

1. Proposed from one or more sources.
2. Appears in `Incubator`.
3. Gets discussed, edited, or rejected.
4. If promising, becomes `shortlisted`.
5. A shortlisted idea may spawn one or more hypotheses.

Expected mutations:

- summary refinement
- risk updates
- status transition

### Hypothesis Lifecycle

1. Drafted from an idea.
2. Refined until success and failure metrics are explicit.
3. Marked `ready`.
4. May be archived if the room decides not to test it.
5. Ready hypotheses can create experiments.

Expected mutations:

- metric refinement
- wording clarification
- readiness transition

### Experiment Lifecycle

1. Created from a ready hypothesis.
2. Linked to one or more shared tasks if execution work is needed.
3. Moves to `running` when work begins.
4. Completes or aborts based on execution outcome.
5. Completion unlocks result recording.

Expected mutations:

- task linking
- owner assignment
- status updates

### Result Lifecycle

1. Recorded after experiment execution.
2. Linked to evidence references.
3. Reviewed by a human or reviewer agent.
4. Marked `validated` or `rejected`.
5. Validated results can influence export or algorithm promotion.

Expected mutations:

- evidence enrichment
- confidence scoring
- validation decision

### Algorithm Lifecycle

1. Proposed from one or more validated results.
2. Enters `candidate` state.
3. Reviewed for scope, preconditions, and limits.
4. Approved by a human or explicit governance override.
5. Optionally published into export artifacts or future playbooks.

Expected mutations:

- procedure refinement
- scope tightening
- approval transition

## Recommended UI Information Hierarchy

The Ladder UI should help users answer three questions quickly:

1. What are we learning?
2. What are we testing now?
3. What is safe to carry into the factory?

Recommended hierarchy in the data panel:

- top summary strip
  - counts by stage
  - active experiments
  - validated results
  - approved algorithms
- middle navigation
  - inbox
  - incubator
  - claims
  - tests
  - findings
  - playbook
- detail pane
  - object metadata
  - linked objects
  - evidence
  - actions

Recommended visible affordances:

- `Promote to hypothesis`
- `Start experiment`
- `Record result`
- `Validate result`
- `Promote algorithm`
- `View linked tasks`

## Summary Generation Guidance

Because the room already exports summaries, Ladder should contribute summary
content in a consistent pyramid.

### One-Line Summary

Purpose:

- quick room status glance

Example:

- `1 active experiment, 2 validated results, 1 algorithm ready for promotion.`

### Short Summary

Purpose:

- operator inbox or dashboard card

Recommended content:

- active experiments
- most important validated result
- any pending approval

### Full Summary

Purpose:

- export artifact or handoff narrative

Recommended content:

- key sources
- shortlisted ideas
- ready hypotheses
- experiment outcomes
- validated results
- promoted algorithms
- approvals still required

## Future Extensions After `v1`

These are reasonable follow-ons after the initial Ladder integration works.

### Cross-Workspace Algorithm Library

Potential addition:

- publish approved algorithms into a reusable library shared across rooms

Why later:

- only makes sense after room-local algorithm quality is proven

### Ladder Templates

Potential addition:

- predefined Ladder workflows for common room types such as debugging,
  performance analysis, or feature ideation

Why later:

- better added after observing repeated usage patterns

### Ladder-Aware Skills

Potential addition:

- packaged agent skills that know how to create and advance Ladder objects

Why later:

- skill design should follow settled domain contracts, not precede them

### Evidence Scoring

Potential addition:

- automatic evidence quality scoring for results

Why later:

- adds complexity to governance before basic result validation is stable

## Final Recommendation

The strongest implementation posture is conservative:

- keep Ladder as a room-level domain in `murmur_demo`
- keep persistence relational and workspace-scoped
- keep the UI projection-based
- keep task execution delegated to `jido_tasks`
- keep export additive and approval-gated
- keep the first slice small

That posture is highly compatible with the existing `morphOS-agent-room`
architecture and gives the software factory a better upstream convergence
surface without introducing a second orchestration system.

## Phased Implementation Plan

### Phase 1: Ladder As Structured Room State

Build:

- schemas and tables for Ladder objects
- context module for CRUD and linking
- one unified Ladder artifact panel
- basic creation and listing tools

Do not build yet:

- advanced auto-promotion logic
- cross-room algorithm libraries
- recursive self-improvement loops

### Phase 2: Ladder To Task Board Bridge

Build:

- experiment-to-task creation
- task status synchronization into experiment status
- result capture prompts after task completion

### Phase 3: Ladder To Export Bridge

Build:

- result and algorithm export files
- summary generation for Ladder outputs
- approval-aware work-order generation

### Phase 4: Ladder To Factory Promotion Discipline

Build:

- algorithm publishing rules
- promotion review packets
- evidence thresholds for downstream adoption

## Anti-Patterns To Avoid

Avoid these designs:

- using `Ladder` as a second room runtime or scheduler
- storing core Ladder state only in chat transcripts
- exporting speculative ideas directly to the software factory
- tying shared Ladder state to one agent session's checkpoint
- auto-promoting algorithms without explicit evidence or approval thresholds

## Recommended `v1` Success Criteria

The `v1` integration should count as successful if:

- a workspace can capture sources, ideas, hypotheses, experiments, results, and
  algorithms as first-class objects
- experiments can link to shared tasks
- results and algorithms can be exported as durable room artifacts
- humans can inspect the whole discovery chain without reading the full chat log
- the software factory receives only validated or explicitly approved outputs

## Final Position

`Ladder` fits `morphOS-agent-room` best as the room's epistemic and discovery
layer.

That means:

- the room becomes better at turning discussion into evidence-backed structure
- the task board becomes the execution layer for tests
- the export connector becomes the gate from discovery into factory action

This preserves the current `morphOS` philosophy while making the room much more
capable as a pre-factory convergence surface.
