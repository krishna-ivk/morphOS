# morphOS v0 Implementation Board

This is the canonical prioritized build board for `morphOS` and the Skyforce repos.

If multiple docs appear to disagree about what comes next, this file wins.

Use it to answer five questions:

- what is still missing
- why it matters
- which upstream or StrongDM idea it comes from
- which repo should own it
- whether it belongs in the MVP, next wave, or defer bucket

## Must Build For MVP

| Feature | Why it matters | Source influence | Repo owner | Status | Priority |
|---|---|---|---|---|---|
| End-to-end delivery spine: `ticket -> workflow -> workspace -> code -> validation -> approval -> promotion` | This is the minimum believable software-factory loop | `morphOS` MVP, `openai/symphony`, StrongDM `seed` and `validation` | `skyforce-symphony`, `skyforce-harness`, `sky-force-command-centre-live`, `skyforce-core` | `in_progress` | `P0` |
| Full `program` and `approval` step execution | The workflow language only becomes real when these steps execute natively and pause or resume correctly | `morphOS` buildability plan, `openai/symphony`, `wavezync/durable` | `skyforce-symphony`, `skyforce-harness`, `sky-force-command-centre-live` | `in_progress` | `P0` |
| Durable checkpoint, resume, and cancel lifecycle | Long-running factory work needs survivability, retries, and controlled recovery | `wavezync/durable` | `skyforce-symphony`, `skyforce-core` | `in_progress` | `P0` |
| Filesystem-first run state and memory layout | Agents and humans need the same inspectable state surface for seeds, plans, artifacts, validation, approvals, and memory | StrongDM `Filesystem` | `morphOS`, `skyforce-core`, `skyforce-symphony` | `in_progress` | `P0` |
| Explicit `interactive` vs `factory` execution mode | The system needs to know when intent is still forming and when it may run to a gate without interruption | StrongDM `Shift Work` | `morphOS`, `skyforce-symphony`, `sky-force-command-centre-live` | `planned` | `P0` |
| Summary pyramid across CLI, dashboard, and artifacts | Operators and agents need one-line, short, full, and evidence-level views of the same run | StrongDM `Pyramid Summaries` | `morphOS`, `skyforce-core`, `skyforce-symphony`, `sky-force-command-centre-live` | `in_progress` | `P1` |
| Universal delivery terminology in operator surfaces | Adoption depends on first-pass comprehensibility; the control plane should read like delivery software, not an internal protocol console | Universal delivery naming work, Paperclip-inspired operator language | `sky-force-command-centre-live`, `morphOS` | `planned` | `P1` |
| Policy hooks at workflow boundaries | Safety and approval semantics need to be enforced at runtime, not just documented | `morphOS` policy model | `skyforce-core`, `skyforce-symphony`, `skyforce-harness` | `planned` | `P1` |
| Event taxonomy alignment across repos | The stack needs one execution language for observability, approvals, and receipts | `morphOS` event model | `skyforce-core`, `skyforce-symphony`, `skyforce-harness`, `sky-force-command-centre-live` | `planned` | `P1` |
| Safe promotion of workspace results back into source repos | A factory loop is incomplete until validated outputs can be proposed or promoted back to the real source tree | `morphOS` MVP, StrongDM `validation` | `skyforce-core`, `skyforce-symphony` | `in_progress` | `P1` |

## Next After MVP

| Feature | Why it matters | Source influence | Repo owner | Status | Priority |
|---|---|---|---|---|---|
| Reference-context retrieval and persistent annotations | This is the next major leverage layer after orchestration and durability | `andrewyng/context-hub` | future context subsystem, `skyforce-core` | `planned` | `P2` |
| Access labels and trust boundaries for context | Memory is only safe if different context types carry explicit authority and visibility boundaries | `morphOS` context architecture, `context-hub` | `skyforce-core` | `in_progress` | `P2` |
| Tool execution behind `ToolAction` contracts | Contracts and observability exist; execution semantics need to catch up | `ComposioHQ/agent-orchestrator` | future tool engine, `skyforce-symphony`, `skyforce-core` | `planned` | `P2` |
| Skill packaging and registration | Skills should become a real reusable subsystem, not just loose references | `openai/skills` | future skill subsystem, `skyforce-core`, `morphOS` | `planned` | `P2` |
| Archetype-to-skill attachment | Agent roles should resolve into concrete skills, permissions, and expected outputs | `openai/skills`, `morphOS` archetypes | `morphOS`, `skyforce-symphony` | `planned` | `P2` |
| Gene Transfusion workflow for cross-repo feature transfer | Reusing working patterns across repos is one of the highest-leverage software-factory moves | StrongDM `Gene Transfusion` | `morphOS`, `skyforce-core`, `skyforce-symphony` | `planned` | `P2` |
| First digital twins for high-risk integrations | Deterministic, high-volume validation becomes much easier once risky integrations are cloned | StrongDM `Digital Twin Universe` | future integration test surfaces, `skyforce-harness` | `planned` | `P2` |
| Stronger operator views for durable state, blocked work, and approvals | The command surface should show what is waiting, why it is blocked, and what a human can do next | Paperclip-like operator control patterns, `durable` | `sky-force-command-centre-live` | `planned` | `P2` |
| Semport discipline for upstream adoption | Upstream ideas should be translated with explicit local ownership instead of copied loosely | StrongDM `Semport` | `morphOS`, `skyforce-core` | `planned` | `P2` |

## Defer

| Feature | Why it is deferred | Source influence | Repo owner | Status |
|---|---|---|---|---|
| Full digital twin coverage for every integration | Valuable, but too broad for the first practical software-factory milestone | StrongDM `Digital Twin Universe` | future integration stack | `deferred` |
| Broad semantic memory platform | The contracts and trust model should stabilize first | `context-hub` plus future memory work | future context subsystem | `deferred` |
| Skill trust and version governance beyond basic registration | Important, but not needed before packaging and attachment exist | `openai/skills` | future skill subsystem | `deferred` |
| Company-OS features like budgets, org charts, and portfolio management | Useful later, but not part of the software-factory-first MVP | Paperclip-style control plane ideas | future operator stack | `deferred` |
| Self-modifying code loops or autonomous policy rewriting | These violate the current trust boundary and validation maturity level | intentionally excluded by `morphOS` doctrine | none yet | `deferred` |

## Repo Ownership Summary

- `morphOS`
  - workflow language
  - execution mode semantics
  - archetypes
  - summary doctrine
  - canonical build priorities
- `skyforce-symphony`
  - orchestration runtime
  - workflow execution semantics
  - durable bridge behavior
  - approval and program step progression
- `skyforce-harness`
  - bounded execution
  - deterministic validation
  - integration validation surfaces
- `skyforce-core`
  - shared contracts
  - policy hooks
  - event taxonomy
  - context and tool-action boundaries
- `sky-force-command-centre-live`
  - operator language
  - approval queue
  - durable-state visibility
  - execution and delivery dashboards

## Decision Rule

When choosing between new work items:

1. prefer items that complete the software-factory loop
2. prefer behavior-first validation over source-only cleverness
3. prefer inspectable filesystem state over hidden memory
4. prefer one canonical contract over duplicated local semantics
5. prefer explicit human authority over implicit automation
