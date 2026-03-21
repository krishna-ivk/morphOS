# P0 Workspace Admin Model Spec

## Origin & Influence
- **Source Influence**: software-factory governance, Paperclip-style operator control, in-house agent patterns
- **Local Owner(s)**: `morphOS`, `skyforce-core`, `sky-force-command-centre-live`, `skyforce-symphony`

## Core Concept
The factory runs with explicit ownership. A `Workspace` maps to a team or repository boundary, and its `Workspace Admin` acts as the definitive human-in-the-loop for local policy failures.

## Responsibilities
- **Approval Targets**: By default, `approval_packet.json` requests scoped to the workspace are routed to the Workspace Admin.
- **Local Rules**: Modifying the context, allowed agent toolset (`ToolAction`), and merge policies for that specific repository.
- **Escalation**: Pushing cross-boundary issues up to the Super Admin.

## Concrete Implementation (Paperclip Operator Controls)
Drawing exactly from `paperclipai/paperclip` design principles, the UI control plane for Workspace Admins must implement:

1. **Policy and Override Visibility**: Workspace Admins must have dashboards specifically isolating "Blocked" tasks waiting for approval, separating them from active or queued work.
2. **Audit-Oriented Navigation**: Actions taken by agents must be projected as a replayable log of events and receipts, rather than a raw "chat window". 
3. **Workspace Isolation**: A Workspace Admin only sees and authorizes activities within their active `workspace_id`, ensuring clear and bounded provenance for any overriding actions they take.
