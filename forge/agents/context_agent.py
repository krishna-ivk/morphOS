import json
import time

def load_all_memory(task):
    """
    Simulates memory bloat. An unoptimized context agent that loads everything.
    """
    print(f"Loading memory for {task['task_id']}...")
    # Simulate loading huge graphs of data
    simulated_context_size = "450MB"
    print(f"Loaded {simulated_context_size} of raw decision traces into memory.")
    return {"status": "retrieval_inefficient", "context_size": simulated_context_size}

def execute_with_context(task):
    """
    Simulates agent execution trying to parse a massive context window.
    """
    context = load_all_memory(task)
    print("Agent struggling to pinpoint relevant context...")
    time.sleep(1) # Simulate slow reasoning over bloated context
    return {
        "plan": "Filter through 450MB of context to find how we fixed date parsers.",
        "patch": "None. Context limit exceeded or agent lost track of instructions.",
        "outcome": "failed"
    }

if __name__ == "__main__":
    with open("../tasks/queue.json", "r") as f:
        tasks = json.load(f)
    print("Running context agent v1...")
    # Run the second task
    for t in tasks:
        if t["task_id"] == "task_002":
            result = execute_with_context(t)
            print(json.dumps(result, indent=2))
