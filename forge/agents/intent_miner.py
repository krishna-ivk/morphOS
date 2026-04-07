def extract_intent(conversation_history):
    """
    Miner responsible for pulling explicit and implicit intent out of triggers.
    In real use, uses an LLM.
    """
    return {
        "intent_confidence_score": 0.87,
        "extracted_constraints": [
            "cost_limit",
            "failure_tolerance"
        ]
    }
