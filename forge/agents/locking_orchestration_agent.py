import json
import threading
import time

# Distributed locking simulator
system_state = {"nodes_patched": 0, "status": "running"}
state_lock = threading.Lock()

def sub_agent_task(agent_id):
    """Simulates a sub-agent applying patches WITH a distributed lock"""
    print(f"[Agent {agent_id}] Requesting A2A lock for state update...")
    
    with state_lock:
        print(f"[Agent {agent_id}] Lock acquired! Checking system state...")
        current_patched = system_state["nodes_patched"]
        time.sleep(0.5)  # Simulate network latency or reasoning time
        
        # Safe update inside the lock
        print(f"[Agent {agent_id}] Applying patch to node {current_patched + 1}...")
        system_state["nodes_patched"] = current_patched + 1
        print(f"[Agent {agent_id}] Releasing lock.")

def orchestrate():
    """Simulates the orchestrator launching concurrent sub-agents"""
    print("Orchestrator splitting task among 3 sub-agents with A2A Locking enabled...")
    threads = []
    
    for i in range(3):
        t = threading.Thread(target=sub_agent_task, args=(i+1,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print(f"Final System State: {system_state}")
    if system_state["nodes_patched"] < 3:
        return {"outcome": "failed", "reason": "Race condition detected."}
    return {"outcome": "success", "nodes_patched": system_state["nodes_patched"]}

if __name__ == "__main__":
    result = orchestrate()
    print(json.dumps(result, indent=2))
