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
| Workspace-scoped admin model | Every workspace needs a named human authority for approvals, local rules, and escalation so the factory can run with clear ownership | software-factory governance, Paperclip-style operator control, in-house agent patterns | `morphOS`, `skyforce-core`, `sky-force-command-centre-live`, `skyforce-symphony` | `planned` | `P0` |
| Super-admin global authority model | Cross-workspace policy, overrides, rollout control, and audit need a higher-trust governance role above individual workspaces | software-factory governance, compliance boundary design | `morphOS`, `skyforce-core`, `sky-force-command-centre-live` | `planned` | `P0` |
| Summary pyramid across CLI, dashboard, and artifacts | Operators and agents need one-line, short, full, and evidence-level views of the same run | StrongDM `Pyramid Summaries` | `morphOS`, `skyforce-core`, `skyforce-symphony`, `sky-force-command-centre-live` | `in_progress` | `P1` |
| Universal delivery terminology in operator surfaces | Adoption depends on first-pass comprehensibility; the control plane should read like delivery software, not an internal protocol console | Universal delivery naming work, Paperclip-inspired operator language | `sky-force-command-centre-live`, `morphOS` | `planned` | `P1` |
| Policy hooks at workflow boundaries | Safety and approval semantics need to be enforced at runtime, not just documented | `morphOS` policy model | `skyforce-core`, `skyforce-symphony`, `skyforce-harness` | `planned` | `P1` |
| Event taxonomy alignment across repos | The stack needs one execution language for observability, approvals, and receipts | `morphOS` event model | `skyforce-core`, `skyforce-symphony`, `skyforce-harness`, `sky-force-command-centre-live` | `planned` | `P1` |
| Safe promotion of workspace results back into source repos | A factory loop is incomplete until validated outputs can be proposed or promoted back to the real source tree | `morphOS` MVP, StrongDM `validation` | `skyforce-core`, `skyforce-symphony` | `in_progress` | `P1` |

## Next After MVP

| Feature | Why it matters | Source influence | Repo owner | Status | Priority |
|---|---|---|---|---|---|
| Follow-up message injection into active runs | Operators should be able to add guidance while work is in flight without restarting the run | `open-swe` | `skyforce-symphony`, `sky-force-command-centre-live` | `planned` | `P2` |
| Deterministic middleware backstops for critical closeout actions | Critical actions like PR creation, summary publication, and approval packet emission should still happen even if the model forgets | `open-swe` | `skyforce-symphony`, `skyforce-core` | `planned` | `P2` |
| Persistent run and thread identity across follow-up messages | Follow-up comments and approvals should route back into the same run context instead of spawning disconnected work | `open-swe` | `skyforce-symphony`, `sky-force-command-centre-live`, `skyforce-core` | `planned` | `P2` |
| Curated tool surface per archetype | Agents should get a small, role-appropriate toolset instead of a sprawling generic tool catalog | `open-swe`, `openai/skills` | `morphOS`, `skyforce-core`, `skyforce-symphony` | `planned` | `P2` |
| Pluggable sandbox boundary | The runtime should be able to swap local and remote execution backends without changing workflow semantics | `open-swe` | `skyforce-symphony`, `skyforce-harness` | `planned` | `P2` |
| Multi-surface invocation parity across Slack, Linear, and GitHub | Work should be invokable from the systems engineers already use without losing run identity or policy semantics | `open-swe` | `skyforce-symphony`, `sky-force-command-centre-live`, future integration surfaces | `planned` | `P2` |
| Workspace admin consoles and approval routing | Workspace admins need dedicated views for blocked work, risky actions, local settings, and escalation queues | operator control plane design, in-house coding-agent patterns | `sky-force-command-centre-live`, `skyforce-core` | `planned` | `P2` |
| Super-admin global control plane | Global admins need cross-workspace policy, audit, workspace provisioning, and rollout controls for skills, tools, and agent capabilities | enterprise agent governance patterns | `sky-force-command-centre-live`, `skyforce-core` | `planned` | `P2` |
| Multi-admin collaboration on a shared run | More than one human should be able to observe or guide a run with clear authorship and authority tracking | Ramp-style multiplayer session model | `skyforce-symphony`, `sky-force-command-centre-live`, `skyforce-core` | `planned` | `P2` |
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
| Fine-grained enterprise org charts beyond workspace and super-admin roles | Useful eventually, but the first governance milestone only needs workspace and global admins | Paperclip-style org modeling | future operator stack | `deferred` |
| Self-modifying code loops or autonomous policy rewriting | These violate the current trust boundary and validation maturity level | intentionally excluded by `morphOS` doctrine | none yet | `deferred` |

## Human Authority Model

The software-factory-first version of `morphOS` should adopt a two-level
human authority model immediately.

### Workspace Admin

Purpose:

- own one workspace, repo group, or delivery surface
- act as the default human approval target for that workspace

Must own now:

- risky-action approvals inside the workspace
- review of blocked or failed runs
- local rule and exemplar curation
- workspace-level tool and capability allowlists
- decision over what may auto-merge vs what requires review

Should not own:

- global policy mutation
- cross-workspace overrides by default
- rollout of new global skills or tools

### Super Admin

Purpose:

- own global platform governance across all workspaces

Must own now:

- global policy
- workspace creation and admin assignment
- approval overrides for exceptional cases
- audit visibility across all workspaces
- rollout approval for new skills, tools, and risky capabilities

Should not do routinely:

- micro-approve every workspace action
- become the only path for normal run completion

### What To Build Now

- workspace identity and admin assignment contract
- super-admin role contract
- approval routing rules:
  - workspace scope defaults to workspace admin
  - cross-workspace or policy-exception scope escalates to super admin
- audit artifacts showing which human role approved what
- operator UI distinction between workspace-admin and super-admin views

### What To Build Next

- delegated admin handoff
- temporary override windows
- multi-admin participation with authorship tracking
- workspace health dashboards and local capability management

### What To Defer

- deep org-chart modeling
- departmental budget trees
- portfolio planning hierarchies beyond workspace grouping

## Agent-Facing Shape Of The Borrowed open-swe Features

These are the Open SWE ideas worth adopting, translated into how they should
feel for agents inside the `morphOS` and Skyforce model.

### 1. Follow-up message injection

How it should work for agents:

- an agent keeps working inside the same run
- if a human adds a Linear comment, Slack reply, or review note mid-run, the runtime injects it before the next agent step
- the agent treats it as new run context, not as a fresh task

What the agent should experience:

- stable run identity
- updated instructions without losing prior artifacts
- fewer abandoned runs when intent changes slightly

### 2. Deterministic closeout middleware

How it should work for agents:

- the agent is still asked to perform normal closeout tasks
- if it forgets a mandatory step, the runtime backstop completes the deterministic part

Examples:

- open draft PR if changes are promotion-ready
- emit `summary_short.md` and `evidence.json` if the agent omitted them
- publish an approval packet when a gated step finishes in a blocked state

What the agent should experience:

- fewer brittle failures from missed housekeeping
- clear separation between creative work and deterministic closeout

### 3. Persistent run and thread identity

How it should work for agents:

- each task gets one durable run identity
- follow-up messages, approvals, and review feedback route into that same run unless the operator explicitly forks it

What the agent should experience:

- one continuing thread of work
- consistent access to prior summaries, receipts, and validation artifacts
- less duplicated planning

### 4. Curated tool surfaces

How it should work for agents:

- each archetype gets a narrow approved toolset
- planners do not get every execution tool
- validators do not get every mutation tool
- releasers only get deployment or publish tools when policy allows

What the agent should experience:

- less tool confusion
- cleaner role boundaries
- more predictable behavior under policy

### 5. Pluggable sandbox boundary

How it should work for agents:

- the agent sees a normal workspace and execution boundary
- the runtime decides whether that boundary is local, containerized, or remote
- workflow semantics stay the same across backends

What the agent should experience:

- consistent behavior across environments
- no need to reason about provider-specific orchestration details

### 6. Multi-surface invocation parity

How it should work for agents:

- the same work order can begin from Slack, Linear, GitHub, or Command Centre
- invocation changes the entry surface, not the core workflow semantics

What the agent should experience:

- consistent run startup shape
- the same policy and summary rules regardless of where the task started

## Design Rule For open-swe Adoption

Adopt the following from `open-swe`:

- invocation symmetry
- threaded follow-ups
- curated tools
- sandbox abstraction
- deterministic middleware backstops

Do not adopt the following wholesale:

- the primary orchestration framework
- prompt-driven validation as the main safety model
- a replacement for the `morphOS defines, Skyforce runs` boundary

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
