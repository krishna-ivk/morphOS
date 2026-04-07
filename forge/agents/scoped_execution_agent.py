import json

ALLOWED_SCOPE = ["utils/date_parser.py"]

def generate_plan():
    """Simulate an agent devising a patch that touches out-of-bounds files"""
    # The agent decides to fix the date parser AND update the test file.
    return {
        "utils/date_parser.py": "def parse(): return '2026-03-23'",
        "tests/test_date_parser.py": "def test_parse(): assert parse() == '2026-03-23'"
    }

def apply_sandboxed_patch(patches):
    """Enforces the strict Scope Constraint identified in Iteration 001"""
    results = {}
    for filepath, content in patches.items():
        print(f"Agent attempting to patch: {filepath}")
        if filepath not in ALLOWED_SCOPE:
            print(f"❌ SECURITY VIOLATION: Agent blocked from editing {filepath}. Scope restricted.")
            results[filepath] = "blocked"
        else:
            print(f"✅ Patch allowed for {filepath}.")
            results[filepath] = "applied"
            
    # If any patches were blocked, the task partially fails
    if "blocked" in results.values():
        return {"outcome": "partial_failure", "reason": "Agent attempted to edit files outside its designated sandbox. Missing permissions for required tests."}
    
    return {"outcome": "success"}

def run_scoped_task(task):
    print(f"Executing {task['task_id']} with strict Sandboxing...")
    print(f"Allowed Scope: {ALLOWED_SCOPE}")
    
    patches = generate_plan()
    outcome = apply_sandboxed_patch(patches)
    return outcome

if __name__ == "__main__":
    with open("../tasks/queue.json", "r") as f:
        tasks = json.load(f)
        
    for t in tasks:
        if t["task_id"] == "task_004":
            result = run_scoped_task(t)
            print(json.dumps(result, indent=2))
