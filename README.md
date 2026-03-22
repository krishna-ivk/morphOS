# morphOS

`morphOS` is the specification and operating-model repository for the long-term agentic system.

Canonical build-priority note: treat [docs/milestones/v0/MORPHOS_V0_IMPLEMENTATION_BOARD.md](docs/milestones/v0/MORPHOS_V0_IMPLEMENTATION_BOARD.md) as the source of truth for what to build next across `morphOS` and Skyforce.

It defines how the platform should think, coordinate, protect itself, and evolve.
It is not the primary runtime.

| Biological System | SkyForce Component | Specification |
|---|---|---|
| **Cell** (atomic unit) | Universal agent template | [cell_spec.md](docs/cell_spec.md) |
| **DNA** (shared blueprint) | Data schemas and contracts | [schemas.md](docs/architecture/schemas.md) |
| **Nervous system** | Event bus (inter-agent communication) | [event_bus_spec.md](docs/architecture/event_bus_spec.md) |
| **Immune system** | Policy engine (safety enforcement) | [policy_engine_spec.md](docs/policy_engine_spec.md) |
| **Brain** | Orchestrator (workflow coordination) | [agentic_os_architecture.md](docs/architecture/agentic_os_architecture.md) |
| **Eyes** | Vision agent | [vision_agent.md](docs/agents/vision_agent.md) |
| **Hands** | Coding agent | [coding_agent.md](docs/agents/coding_agent.md) |
| **White blood cells** | Debugging agent | [debugging_agent.md](docs/agents/debugging_agent.md) |
| **Skeleton inspector** | Architecture agent | [architecture_agent.md](docs/agents/architecture_agent.md) |
| **Hippocampus** | Learning agent | [learning_agent.md](docs/agents/learning_agent.md) |
| **Symbiont cells** | Human roles (21 roles) | [human_cell_spec.md](docs/human_cell_spec.md) |
| **Genome** | Product vision | [product_vision.md](docs/vision/product_vision.md) |
| **Muscles** | Programs and scripts | `programs/`, `scripts/` |
| **Long-term memory** | Capability store | `memory/capability_store.json` |
| **Circulatory system** | Workflow pipelines | `workflows/` |

That role belongs to the Skyforce repos:

- `skyforce-symphony`: orchestration runtime
- `skyforce-harness`: execution and adapter runtime
- `skyforce-command-centre`: operator control plane
- `skyforce-core`: shared contracts, CLI, and validation surface

See [agentic_os_architecture.md](docs/architecture/agentic_os_architecture.md) for the full system design.
Use [docs/README.md](docs/README.md) as the documentation index.

## Start Here

If you are reading this as a human operator, builder, or collaborator, use this order:

1. [Human guide](docs/HUMAN_GUIDE.md)
2. [Skyforce runtime overview](docs/SKYFORCE_RUNTIME_OVERVIEW.md)
3. [Buildability plan](docs/morphos_buildability_plan.md)
4. [morphOS vs Skyforce evaluation](docs/morphos_vs_skyforce_evaluation.md)
5. [morphOS v0 core stack](docs/milestones/v0/MORPHOS_V0_CORE_STACK.md)
6. [morphOS v0 runtime contracts](docs/milestones/v0/MORPHOS_V0_RUNTIME_CONTRACTS.md)
7. [Symphony and Durable authority boundary](docs/architecture/SYMPHONY_DURABLE_AUTHORITY_BOUNDARY.md)
8. [Durable execution handoff contracts](docs/architecture/DURABLE_EXECUTION_HANDOFF_CONTRACTS.md)
9. [morphOS v0 upstream adoption map](docs/milestones/v0/MORPHOS_V0_UPSTREAM_ADOPTION_MAP.md)
10. [morphOS v0 upstream feature backlog](docs/milestones/v0/MORPHOS_V0_UPSTREAM_FEATURE_BACKLOG.md)
11. [Starred repo gene transfusion backlog](docs/STARRED_REPO_GENE_TRANSFUSION_BACKLOG.md)
12. [Gene transfusion from ACE platform](docs/GENE_TRANSFUSION_FROM_ACE_PLATFORM.md)
13. [Agent signal and action model](docs/core-mechanics/AGENT_SIGNAL_AND_ACTION_MODEL.md)
14. [Git native work ledger spec](docs/core-mechanics/GIT_NATIVE_WORK_LEDGER_SPEC.md)
15. [Filesystem memory topology spec](docs/core-mechanics/FILESYSTEM_MEMORY_TOPOLOGY_SPEC.md)
16. [Tool registry and action discovery spec](docs/core-mechanics/TOOL_REGISTRY_AND_ACTION_DISCOVERY_SPEC.md)
17. [Tool execution engine spec](docs/core-mechanics/TOOL_EXECUTION_ENGINE_SPEC.md)
18. [Software factory control flow spec](docs/core-mechanics/SOFTWARE_FACTORY_CONTROL_FLOW_SPEC.md)
19. [Workflow pack and registry spec](docs/workflows/WORKFLOW_PACK_AND_REGISTRY_SPEC.md)
20. [Validation guardrails and review loop spec](docs/core-mechanics/VALIDATION_GUARDRAILS_AND_REVIEW_LOOP_SPEC.md)
21. [Digital twin validation spec](docs/core-mechanics/DIGITAL_TWIN_VALIDATION_SPEC.md)
22. [Pyramid summary rendering spec](docs/core-mechanics/PYRAMID_SUMMARY_RENDERING_SPEC.md)
23. [Policy hooks at workflow boundaries spec](docs/core-mechanics/POLICY_HOOKS_AT_WORKFLOW_BOUNDARIES_SPEC.md)
24. [Gene transfusion equivalence spec](docs/core-mechanics/GENE_TRANSFUSION_EQUIVALENCE_SPEC.md)
25. [Shift work execution semantics spec](docs/core-mechanics/SHIFT_WORK_EXECUTION_SEMANTICS_SPEC.md)
26. [Workspace admin governance spec](docs/core-mechanics/WORKSPACE_ADMIN_GOVERNANCE_SPEC.md)
27. [Parallel workspace execution spec](docs/core-mechanics/PARALLEL_WORKSPACE_EXECUTION_SPEC.md)
28. [Semport adoption boundary spec](docs/core-mechanics/SEMPORT_ADOPTION_BOUNDARY_SPEC.md)
29. [Code intelligence retrieval spec](docs/core-mechanics/CODE_INTELLIGENCE_RETRIEVAL_SPEC.md)
30. [Token and command mediation spec](docs/core-mechanics/TOKEN_AND_COMMAND_MEDIATION_SPEC.md)
31. [Digital twin universe rollout spec](docs/core-mechanics/DIGITAL_TWIN_UNIVERSE_ROLLOUT_SPEC.md)
32. [Review loop automation spec](docs/core-mechanics/REVIEW_LOOP_AUTOMATION_SPEC.md)
33. [Token economy and observability spec](docs/core-mechanics/TOKEN_ECONOMY_AND_OBSERVABILITY_SPEC.md)
34. [Skill packaging and registration spec](docs/core-mechanics/SKILL_PACKAGING_AND_REGISTRATION_SPEC.md)
35. [Context Hub runtime integration spec](docs/architecture/CONTEXT_HUB_RUNTIME_INTEGRATION_SPEC.md)
36. [Eval driven acceptance spec](docs/core-mechanics/EVAL_DRIVEN_ACCEPTANCE_SPEC.md)
37. [Upstream drift monitoring spec](docs/core-mechanics/UPSTREAM_DRIFT_MONITORING_SPEC.md)
38. [Reference context promotion spec](docs/core-mechanics/REFERENCE_CONTEXT_PROMOTION_SPEC.md)
39. [Workflow acceptance profile spec](docs/workflows/WORKFLOW_ACCEPTANCE_PROFILE_SPEC.md)
40. [Drift response playbook spec](docs/core-mechanics/DRIFT_RESPONSE_PLAYBOOK_SPEC.md)
41. [Memory governance and retention spec](docs/core-mechanics/MEMORY_GOVERNANCE_AND_RETENTION_SPEC.md)
42. [Workflow profile compatibility spec](docs/workflows/WORKFLOW_PROFILE_COMPATIBILITY_SPEC.md)
43. [Reference context staleness and refresh spec](docs/core-mechanics/REFERENCE_CONTEXT_STALENESS_AND_REFRESH_SPEC.md)
44. [Pack migration and deprecation spec](docs/core-mechanics/PACK_MIGRATION_AND_DEPRECATION_SPEC.md)
45. [Active run policy reevaluation spec](docs/core-mechanics/ACTIVE_RUN_POLICY_REEVALUATION_SPEC.md)
46. [Workflow policy profile spec](docs/workflows/WORKFLOW_POLICY_PROFILE_SPEC.md)
47. [Workflow profile resolution spec](docs/workflows/WORKFLOW_PROFILE_RESOLUTION_SPEC.md)
48. [Workflow profile override governance spec](docs/workflows/WORKFLOW_PROFILE_OVERRIDE_GOVERNANCE_SPEC.md)
49. [Workflow profile change management spec](docs/workflows/WORKFLOW_PROFILE_CHANGE_MANAGEMENT_SPEC.md)
50. [Workflow profile observability spec](docs/workflows/WORKFLOW_PROFILE_OBSERVABILITY_SPEC.md)
51. [Workflow profile recommendation spec](docs/workflows/WORKFLOW_PROFILE_RECOMMENDATION_SPEC.md)
52. [Workflow profile simulation and sandbox spec](docs/workflows/WORKFLOW_PROFILE_SIMULATION_AND_SANDBOX_SPEC.md)
53. [Agent archetype skill attachment spec](docs/architecture/AGENT_ARCHETYPE_SKILL_ATTACHMENT_SPEC.md)
51. [Profile doctrine conflict resolution spec](docs/doctrines/PROFILE_DOCTRINE_CONFLICT_RESOLUTION_SPEC.md)
52. [Profile doctrine stability and freeze spec](docs/doctrines/PROFILE_DOCTRINE_STABILITY_AND_FREEZE_SPEC.md)
53. [Profile doctrine wave launch spec](docs/doctrines/PROFILE_DOCTRINE_WAVE_LAUNCH_SPEC.md)
54. [Profile doctrine post wave retrospective spec](docs/doctrines/PROFILE_DOCTRINE_POST_WAVE_RETROSPECTIVE_SPEC.md)
55. [Profile doctrine multi wave learning spec](docs/doctrines/PROFILE_DOCTRINE_MULTI_WAVE_LEARNING_SPEC.md)
56. [Profile doctrine maturity model spec](docs/doctrines/PROFILE_DOCTRINE_MATURITY_MODEL_SPEC.md)
57. [Profile doctrine maturity advancement playbook spec](docs/doctrines/PROFILE_DOCTRINE_MATURITY_ADVANCEMENT_PLAYBOOK_SPEC.md)
58. [Profile doctrine regression response spec](docs/doctrines/PROFILE_DOCTRINE_REGRESSION_RESPONSE_SPEC.md)
59. [Software factory techniques for morphOS](docs/SOFTWARE_FACTORY_TECHNIQUES_FOR_MORPHOS.md)
60. [Context architecture](docs/architecture/CONTEXT_ARCHITECTURE.md)
61. [Context Hub evaluation](docs/core-mechanics/CONTEXT_HUB_EVALUATION.md)
62. [Context Hub integration plan](docs/core-mechanics/CONTEXT_HUB_INTEGRATION_PLAN.md)
63. [Roadmap](docs/ROADMAP.md)

## What morphOS Owns

`morphOS` should own:

- the operating model
- workflow language
- policy language
- agent archetypes
- runtime topology definitions
- safe evolution direction

It should not own:

- the main orchestration runtime
- the main event bus runtime
- node execution
- the operator UI

## Current Relationship To Skyforce

The current platform model is:

- `morphOS` defines the organism
- Skyforce runs the organism

That boundary matters. It keeps architecture and runtime from drifting into two overlapping systems.

## What Is Already Real In Skyforce

The Skyforce runtime already implements several `morphOS`-aligned pieces:

- workflow template loading from `morphOS/workflows`
- template selection inside Symphony
- lightweight workflow progress tracking
- runtime-action classification for current steps
- execution envelopes and receipts carrying workflow metadata
- CLI and dashboard visibility for that progress

## Key Docs

- [Agentic OS architecture](docs/architecture/agentic_os_architecture.md)
- [Cell spec](docs/cell_spec.md)
- [Schemas](docs/architecture/schemas.md)
- [Event bus spec](docs/architecture/event_bus_spec.md)
- [Policy engine spec](docs/policy_engine_spec.md)
- [Runtime topology spec](docs/architecture/runtime_topology_spec.md)
- [Interaction layer spec](docs/interaction_layer_spec.md)
- [morphOS v0 core stack](docs/milestones/v0/MORPHOS_V0_CORE_STACK.md)
- [morphOS v0 runtime contracts](docs/milestones/v0/MORPHOS_V0_RUNTIME_CONTRACTS.md)
- [Symphony and Durable authority boundary](docs/architecture/SYMPHONY_DURABLE_AUTHORITY_BOUNDARY.md)
- [Durable execution handoff contracts](docs/architecture/DURABLE_EXECUTION_HANDOFF_CONTRACTS.md)
- [morphOS v0 upstream adoption map](docs/milestones/v0/MORPHOS_V0_UPSTREAM_ADOPTION_MAP.md)
- [morphOS v0 upstream feature backlog](docs/milestones/v0/MORPHOS_V0_UPSTREAM_FEATURE_BACKLOG.md)
- [Starred repo gene transfusion backlog](docs/STARRED_REPO_GENE_TRANSFUSION_BACKLOG.md)
- [Agent signal and action model](docs/core-mechanics/AGENT_SIGNAL_AND_ACTION_MODEL.md)
- [Git native work ledger spec](docs/core-mechanics/GIT_NATIVE_WORK_LEDGER_SPEC.md)
- [Filesystem memory topology spec](docs/core-mechanics/FILESYSTEM_MEMORY_TOPOLOGY_SPEC.md)
- [Tool registry and action discovery spec](docs/core-mechanics/TOOL_REGISTRY_AND_ACTION_DISCOVERY_SPEC.md)
- [Software factory control flow spec](docs/core-mechanics/SOFTWARE_FACTORY_CONTROL_FLOW_SPEC.md)
- [Workflow pack and registry spec](docs/workflows/WORKFLOW_PACK_AND_REGISTRY_SPEC.md)
- [Validation guardrails and review loop spec](docs/core-mechanics/VALIDATION_GUARDRAILS_AND_REVIEW_LOOP_SPEC.md)
- [Digital twin validation spec](docs/core-mechanics/DIGITAL_TWIN_VALIDATION_SPEC.md)
- [Pyramid summary rendering spec](docs/core-mechanics/PYRAMID_SUMMARY_RENDERING_SPEC.md)
- [Policy hooks at workflow boundaries spec](docs/core-mechanics/POLICY_HOOKS_AT_WORKFLOW_BOUNDARIES_SPEC.md)
- [Gene transfusion equivalence spec](docs/core-mechanics/GENE_TRANSFUSION_EQUIVALENCE_SPEC.md)
- [Shift work execution semantics spec](docs/core-mechanics/SHIFT_WORK_EXECUTION_SEMANTICS_SPEC.md)
- [Workspace admin governance spec](docs/core-mechanics/WORKSPACE_ADMIN_GOVERNANCE_SPEC.md)
- [Parallel workspace execution spec](docs/core-mechanics/PARALLEL_WORKSPACE_EXECUTION_SPEC.md)
- [Semport adoption boundary spec](docs/core-mechanics/SEMPORT_ADOPTION_BOUNDARY_SPEC.md)
- [Code intelligence retrieval spec](docs/core-mechanics/CODE_INTELLIGENCE_RETRIEVAL_SPEC.md)
- [Token and command mediation spec](docs/core-mechanics/TOKEN_AND_COMMAND_MEDIATION_SPEC.md)
- [Digital twin universe rollout spec](docs/core-mechanics/DIGITAL_TWIN_UNIVERSE_ROLLOUT_SPEC.md)
- [Review loop automation spec](docs/core-mechanics/REVIEW_LOOP_AUTOMATION_SPEC.md)
- [Token economy and observability spec](docs/core-mechanics/TOKEN_ECONOMY_AND_OBSERVABILITY_SPEC.md)
- [Context Hub runtime integration spec](docs/architecture/CONTEXT_HUB_RUNTIME_INTEGRATION_SPEC.md)
- [Eval driven acceptance spec](docs/core-mechanics/EVAL_DRIVEN_ACCEPTANCE_SPEC.md)
- [Upstream drift monitoring spec](docs/core-mechanics/UPSTREAM_DRIFT_MONITORING_SPEC.md)
- [Reference context promotion spec](docs/core-mechanics/REFERENCE_CONTEXT_PROMOTION_SPEC.md)
- [Workflow acceptance profile spec](docs/workflows/WORKFLOW_ACCEPTANCE_PROFILE_SPEC.md)
- [Work order schema spec](docs/core-mechanics/WORK_ORDER_SCHEMA_SPEC.md)
- [Agent archetypes spec](docs/architecture/AGENT_ARCHETYPES_SPEC.md)
- [Approval packet schema spec](docs/core-mechanics/APPROVAL_PACKET_SCHEMA_SPEC.md)
- [Execution receipt schema spec](docs/core-mechanics/EXECUTION_RECEIPT_SCHEMA_SPEC.md)
- [MVP workflow behavior spec](docs/core-mechanics/MVP_WORKFLOW_BEHAVIOR_SPEC.md)
- [P0 factory spine recovery plan](docs/milestones/P0/P0_FACTORY_SPINE_RECOVERY_PLAN.md)
- [P0 factory spine implementation checklist](docs/milestones/P0/P0_FACTORY_SPINE_IMPLEMENTATION_CHECKLIST.md)
- [P1 event taxonomy spec](docs/milestones/P1/P1_EVENT_TAXONOMY_SPEC.md)
- [P1 policy hooks spec](docs/milestones/P1/P1_POLICY_HOOKS_SPEC.md)
- [P1 safe promotion spec](docs/milestones/P1/P1_SAFE_PROMOTION_SPEC.md)
- [P1 summary pyramid spec](docs/milestones/P1/P1_SUMMARY_PYRAMID_SPEC.md)
- [P1 universal terminology spec](docs/milestones/P1/P1_UNIVERSAL_TERMINOLOGY_SPEC.md)
- [Software factory techniques for morphOS](docs/SOFTWARE_FACTORY_TECHNIQUES_FOR_MORPHOS.md)
- [Context architecture](docs/architecture/CONTEXT_ARCHITECTURE.md)
- [Context Hub evaluation](docs/core-mechanics/CONTEXT_HUB_EVALUATION.md)
- [Context Hub integration plan](docs/core-mechanics/CONTEXT_HUB_INTEGRATION_PLAN.md)
- [Profile doctrine recovery and requalification spec](docs/doctrines/PROFILE_DOCTRINE_RECOVERY_AND_REQUALIFICATION_SPEC.md)
- [Profile doctrine reentry and expansion spec](docs/doctrines/PROFILE_DOCTRINE_REENTRY_AND_EXPANSION_SPEC.md)
- [Profile doctrine trust decay spec](docs/doctrines/PROFILE_DOCTRINE_TRUST_DECAY_SPEC.md)
- [Profile doctrine renewal and recertification spec](docs/doctrines/PROFILE_DOCTRINE_RENEWAL_AND_RECERTIFICATION_SPEC.md)
- [Profile doctrine portfolio health spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_HEALTH_SPEC.md)
- [Profile doctrine portfolio intervention spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_INTERVENTION_SPEC.md)
- [Profile doctrine portfolio exit criteria spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_EXIT_CRITERIA_SPEC.md)
- [Profile doctrine portfolio reentry spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_REENTRY_SPEC.md)
- [Profile doctrine portfolio baseline spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_BASELINE_SPEC.md)
- [Profile doctrine portfolio SLO and alerting spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_SLO_AND_ALERTING_SPEC.md)
- [Profile doctrine portfolio capacity and load spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_CAPACITY_AND_LOAD_SPEC.md)
- [Profile doctrine portfolio triage policy spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_TRIAGE_POLICY_SPEC.md)
- [Profile doctrine portfolio escalation policy spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_ESCALATION_POLICY_SPEC.md)
- [Profile doctrine portfolio decision authority spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_DECISION_AUTHORITY_SPEC.md)
- [Profile doctrine portfolio decision audit spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_DECISION_AUDIT_SPEC.md)
- [Profile doctrine portfolio review cadence spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_REVIEW_CADENCE_SPEC.md)
- [Profile doctrine portfolio exception handling spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_EXCEPTION_HANDLING_SPEC.md)
- [Profile doctrine portfolio continuity and failsafe spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_CONTINUITY_AND_FAILSAFE_SPEC.md)
- [Profile doctrine portfolio recovery from failsafe spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_RECOVERY_FROM_FAILSAFE_SPEC.md)
- [Profile doctrine portfolio maturity scorecard spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_MATURITY_SCORECARD_SPEC.md)
- [Profile doctrine portfolio scorecard calibration spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_CALIBRATION_SPEC.md)
- [Profile doctrine portfolio scorecard governance spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_GOVERNANCE_SPEC.md)
- [Profile doctrine portfolio scorecard publication spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_PUBLICATION_SPEC.md)
- [Profile doctrine portfolio scorecard retention and history spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_RETENTION_AND_HISTORY_SPEC.md)
- [Profile doctrine portfolio scorecard consumption policy spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_CONSUMPTION_POLICY_SPEC.md)
- [Profile doctrine portfolio scorecard exception spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_EXCEPTION_SPEC.md)
- [Profile doctrine portfolio scorecard reconciliation spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_RECONCILIATION_SPEC.md)
- [Profile doctrine portfolio scorecard decision binding spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_DECISION_BINDING_SPEC.md)
- [Profile doctrine portfolio scorecard action protocol spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_ACTION_PROTOCOL_SPEC.md)
- [Profile doctrine portfolio scorecard automation boundary spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_AUTOMATION_BOUNDARY_SPEC.md)
- [Profile doctrine portfolio scorecard operator handoff spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_OPERATOR_HANDOFF_SPEC.md)
- [Profile doctrine portfolio scorecard queue discipline spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_QUEUE_DISCIPLINE_SPEC.md)
- [Profile doctrine portfolio scorecard SLA and breach response spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_SLA_AND_BREACH_RESPONSE_SPEC.md)
- [Profile doctrine portfolio scorecard capacity recovery spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_CAPACITY_RECOVERY_SPEC.md)
- [Profile doctrine portfolio scorecard load shedding spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_SCORECARD_LOAD_SHEDDING_SPEC.md)
- [Profile doctrine portfolio shed backlog reactivation spec](docs/doctrines/PROFILE_DOCTRINE_PORTFOLIO_SHED_BACKLOG_REACTIVATION_SPEC.md)
- [P0 golden path seed packet](docs/milestones/P0/P0_GOLDEN_PATH_SEED_PACKET.md)

## Current Release

Current specification release line:

- `0.1.0`

This is a specification baseline, not a production runtime release.
