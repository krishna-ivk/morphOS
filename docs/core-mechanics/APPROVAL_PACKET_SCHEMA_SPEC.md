# Approval Packet Schema Spec

## Meaning
The `approval_packet.json` is a structured document emitted when the control flow reaches an explicit human authority gate (e.g. `review_gate`, `promotion_gate`). It specifies what decision needs to be made, exactly who has the authority to make it, and the objective evidence supporting the decision.

## Governance
This artifact is the sole mechanism by which human operators intervene during paused or gated workflow steps. A simple "yes/no" click in an operator UI must produce an `approval_decision.json` that directly answers this packet.

## Schema Payload

Produced by: `Review Archetype` / `Validation Handoff`
Consumed by: `skyforce-command-centre-live` (Human UI), `skyforce-api-gateway` (Operator API layer), `skyforce-symphony` (Resuming Orchestrator)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["packet_id", "run_id", "gate_type", "authority_scope", "status", "requested_at"],
  "properties": {
    "packet_id": { "type": "string" },
    "run_id": { "type": "string" },
    "issue_identifier": { "type": "string" },
    
    "gate_type": {
      "type": "string",
      "enum": ["plan_gate", "tool_gate", "validation_gate", "review_gate", "promotion_gate"]
    },
    
    "authority_scope": {
      "type": "string",
      "enum": ["workspace_admin", "super_admin"]
    },
    
    "status": {
      "type": "string",
      "enum": ["pending", "approved", "rejected", "rework_requested", "escalated"]
    },

    "requested_at": { "type": "string", "format": "date-time" },
    "resolved_at": { "type": "string", "format": "date-time" },
    "resolved_by_user": { "type": "string" },
    "resolution_reason": { "type": "string" },

    "context": {
      "type": "object",
      "properties": {
        "summary_short_ref": { "type": "string" },
        "summary_full_ref": { "type": "string" },
        "evidence_ref": { "type": "string", "description": "Pointer to task_evidence.json" }
      }
    },
    
    "proposed_action": {
      "type": "string",
      "description": "What exactly will happen if this is approved (e.g. 'Merge Branch feature/x', 'Publish Npm Package')"
    }
  }
}
```

## Why This Matters
If approvals are strictly tied to structured packets rather than UI state, runs become auditable. You can replay the history and see `packet_id: 456` was approved by `workspace_admin_id: shiva` at `2026-03-21T...` with the justification "Looks solid."
