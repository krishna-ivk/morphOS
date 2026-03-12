# SkyForce — AI Software Factory as a Living Organism

An autonomous software engineering operating system modeled as a biological organism.

## The Organism Metaphor

| Biological System | SkyForce Component | Specification |
|---|---|---|
| **Cell** (atomic unit) | Universal agent template | [cell_spec.md](docs/cell_spec.md) |
| **DNA** (shared blueprint) | Data schemas and contracts | [schemas.md](docs/schemas.md) |
| **Nervous system** | Event bus (inter-agent communication) | [event_bus_spec.md](docs/event_bus_spec.md) |
| **Immune system** | Policy engine (safety enforcement) | [policy_engine_spec.md](docs/policy_engine_spec.md) |
| **Brain** | Orchestrator (workflow coordination) | [agentic_os_architecture.md](docs/agentic_os_architecture.md) |
| **Eyes** | Vision agent | [vision_agent.md](agents/vision_agent.md) |
| **Hands** | Coding agent | [coding_agent.md](agents/coding_agent.md) |
| **White blood cells** | Debugging agent | [debugging_agent.md](agents/debugging_agent.md) |
| **Skeleton inspector** | Architecture agent | [architecture_agent.md](agents/architecture_agent.md) |
| **Hippocampus** | Learning agent | [learning_agent.md](agents/learning_agent.md) |
| **Symbiont cells** | Human roles (21 roles) | [human_cell_spec.md](docs/human_cell_spec.md) |
| **Genome** | Product vision | [product_vision.md](vision/product_vision.md) |
| **Muscles** | Programs and scripts | `programs/`, `scripts/` |
| **Long-term memory** | Capability store | `memory/capability_store.json` |
| **Circulatory system** | Workflow pipelines | `workflows/` |

## Architecture

See [agentic_os_architecture.md](docs/agentic_os_architecture.md) for the full system design.

## Quick Start

Run the feature pipeline:
```bash
codex run workflows/feature_pipeline.yaml
```

Evaluate a repository:
```bash
codex run workflows/repo_evaluation.yaml
```

## Project Structure

```
skyforce/
├── agents/               # Organ definitions (all follow cell_spec.md)
│   ├── vision_agent.md
│   ├── coding_agent.md
│   ├── debugging_agent.md
│   ├── architecture_agent.md
│   └── learning_agent.md
├── docs/                 # System specifications
│   ├── cell_spec.md           # The universal cell template
│   ├── schemas.md             # Shared data contracts (DNA)
│   ├── event_bus_spec.md      # Nervous system
│   ├── policy_engine_spec.md  # Immune system
│   └── agentic_os_architecture.md  # Full OS architecture
├── memory/               # Long-term memory
│   └── capability_store.json
├── programs/             # Deterministic tools (muscles)
│   ├── run_tests.sh
│   ├── repo_scan.sh
│   ├── dependency_scan.sh
│   └── deploy.sh
├── scripts/              # Helper scripts
│   └── task_split.py
├── vision/               # Genome
│   └── product_vision.md
├── workflows/            # Circulatory pipelines
│   ├── feature_pipeline.yaml
│   ├── repo_evaluation.yaml
│   └── release_pipeline.yaml
└── AGENTS.md             # Agent operating rules
```

## Design Principles

1. **Every agent is a cell** — grown from the same template, with mandatory inputs, outputs, failure modes, and health reporting
2. **No direct agent-to-agent calls** — all communication flows through the event bus
3. **Default deny** — the policy engine blocks unlisted actions
4. **Offline-first** — the system works without internet; connectivity amplifies, not enables
5. **Learn from every run** — the learning agent extracts and stores reusable knowledge
