# Context Hub Maturity Plan

## Current State (v1)

Context is currently "split" between:
- **Doctrine**: `CONTEXT_ARCHITECTURE.md` defines the three layers (Reference, Operational, Persistent Memory).
- **Runtime**: `skyforce-core` has `ContextRef` contracts and `RepoDocContextProvider`.
- **Command Centre**: Ad-hoc context retrieval for issue summaries and run bundles.
- **Harness**: Context-embedding during `execution-envelope` generation.

## Objective

Move the Context Hub from a "local helper library" to a **Dedicated Shared Subsystem (V2)**. This ensures that memory is consistently delivered across repositories and avoids the "context drift" where Symphony and Command Centre have different views of the same issue.

## Phase 2 Architecture

The **Context Hub Service** will own:
1. **Consolidated Retrieval**: A single API endpoint to fetch context across all providers (Git docs, JSON artifacts, and persistent memory).
2. **Context Compression**: Automated synthesis of long run-histories into compact "Operational Insights" for future agents.
3. **Cross-Repo Context Handover**: Orchestrating how a "Reference Context" (from `morphOS`) becomes an "Operational Context" (in `skyforce-symphony`) and eventually a "Memory Asset".
4. **Knowledge Item (KI) Integration**: Bringing the repo-local knowledge system (`KIs`) into the live runtime's inference pathway.

## Key Subsystems

### 1. Unified Context Provider Interface
Move toward a more structured registry of context providers:
- `GitProvider`: Documents and READMEs.
- `ArtifactProvider`: Receipts, approvals, and validation results.
- `MemoryProvider`: Long-term playbook outcomes and exemplars.
- `ExternalProvider`: Linear/Slack/Issues.

### 2. Context Synthesis (Compression)
Implement "Context Folding" where extremely long operational logs are synthesized into a single `OperationalSummary` artifact before being fed into a new run's context.

### 3. Identity and Authorization
Ensure context retrieval respects the **Human Authority Model**. Sensitive context (e.g., deployment secrets or audit logs) should require `admin` or higher roles for retrieval.

## Implementation Steps

1. **Service Extraction**: Extract `RepoDocContextProvider` and related logic into a standalone `skyforce-context-hub` service. ✅ DONE — Express service on port 3005 with search, get, list-annotations, create-annotation endpoints.
2. **Protocol Standard**: Define an HTTP/gRPC protocol for requesting context using `ContextRef` as the key. ✅ DONE — HTTP REST protocol defined and implemented; API gateway proxies all context operations through Context Hub with `sky` CLI fallback.
3. **Agent Integration**: Update `skyforce-harness` to fetch context-blobs from the Service instead of resolving them through filesystem/CLI. ✅ DONE — harness already treats `context_refs` as opaque references and carries them through the pipeline; context resolution happens upstream via API gateway → Context Hub.
4. **Retention Policy**: Implement the "Reference -> Operational -> Memory" promotion path. ⏳ PENDING — Context Compression (Phase 2.2) and Cross-Repo Context Handover (Phase 2.3) remain.
