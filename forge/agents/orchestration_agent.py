import json
import threading
import time

system_state = {"nodes_patched": 0, "status": "running"}

def sub_agent_task(agent_id):
    """Simulates a sub-agent blindly applying patches without locking"""
    print(f"[Agent {agent_id}] Checking system state...")
    current_patched = system_state["nodes_patched"]
    time.sleep(0.5)  # Simulate network latency or reasoning time
    
    # Race condition: Multiple agents read the same ancient state
    print(f"[Agent {agent_id}] Applying patch to node {current_patched + 1}...")
    system_state["nodes_patched"] = current_patched + 1

def orchestrate():
    """Simulates the orchestrator launching concurrent sub-agents"""
    print("Orchestrator splitting task among 3 sub-agents...")
    threads = []
    
    for i in range(3):
        t = threading.Thread(target=sub_agent_task, args=(i+1,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print(f"Final System State: {system_state}")
    if system_state["nodes_patched"] < 3:
        return {"outcome": "failed", "reason": "Race condition detected: agents overwrote each other's state updates."}
    return {"outcome": "success"}

if __name__ == "__main__":
    result = orchestrate()
    print(json.dumps(result, indent=2))
