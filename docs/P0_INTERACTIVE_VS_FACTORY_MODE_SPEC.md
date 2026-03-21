# P0 Interactive vs Factory Execution Mode Spec

## Origin & Influence
- **Source Influence**: StrongDM `Shift Work`
- **Local Owner(s)**: `morphOS`, `skyforce-symphony`, `sky-force-command-centre-live`

## Core Concept
The orchestration engine (`skyforce-symphony`) and the UI (`sky-force-command-centre-live`) need explicit boundaries defining when an agent is brainstorming with a human vs when it is executing a locked pipeline.

## Modes
1. **Interactive Mode**:
   - Intent is still forming.
   - The agent is allowed to act conversationally, ask clarifying questions frequently, and stream intermediate thoughts.
   - Analogue: Pair programming.

2. **Factory Mode (`Shift Work`)**:
   - The `work_order` is locked and approved.
   - The workflow executes head-down without pinging the operator until it hits a pre-defined gating policy (e.g. `promotion_gate`).
   - Analogue: Pushing a build to CI/CD.

## Concrete Implementation (Shift Work Semantics)
Based on upstream *Shift Work* patterns, the platform implements these concrete execution rules:

**Interrupt Strategy**:
- Interactive: Interrupt early when scope is unclear, multiple paths exist, or operator preference matters.
- Factory: Do not interrupt for deterministic work. Interrupt ONLY on policy blockers, required human approval gates, or exhausted retry budgets.

**Summaries & Transparency**:
- Interactive runs prioritize projecting ambiguity, pending decisions, and next discussion points to the operator.
- Factory runs suppress conversational noise and prioritize status projection (executing vs blocked) and final validation receipts.

**Mode Inference and Enums**:
- The runtime explicitly tracks `execution_mode`, `execution_mode_source` (inferred vs declared), and `execution_mode_locked`.
- The system must never silently drift modes; mode changes (`run.mode_changed`) must be logged events in the durable execution envelope.
