import json
import threading
import time

system_state = {"nodes_patched": 0, "status": "running"}
# A mock distributed TTL Lock
# dict showing: {"owner": agent_id, "expires_at": timestamp}
distributed_lock = {"owner": None, "expires_at": 0}
LOCK_TIMEOUT = 1.0  # 1 second TTL

def acquire_lock(agent_id):
    """Attempt to acquire a TTL lease on the state."""
    print(f"[Agent {agent_id}] Attempting to acquire lease...")
    while True:
        now = time.time()
        # If lock is free or expired -> Grab it
        if distributed_lock["owner"] is None or distributed_lock["expires_at"] < now:
            if distributed_lock["owner"] is not None:
                print(f"[Agent {agent_id}] Previous lock expired (Deadlock busted)! Reclaiming lease...")
            distributed_lock["owner"] = agent_id
            distributed_lock["expires_at"] = now + LOCK_TIMEOUT
            print(f"[Agent {agent_id}] Lease acquired. Expires in {LOCK_TIMEOUT}s.")
            return True
        time.sleep(0.5)

def release_lock(agent_id):
    if distributed_lock["owner"] == agent_id:
        distributed_lock["owner"] = None
        print(f"[Agent {agent_id}] Lease released safely.")

def sub_agent_task(agent_id, should_crash=False):
    """Simulates a sub-agent applying patches"""
    acquire_lock(agent_id)
    
    current_patched = system_state["nodes_patched"]
    
    if should_crash:
        print(f"[Agent {agent_id}] FATAL EXCEPTION: Agent crashed mid-execution!")
        # Agent dies BEFORE releasing lock
        return
        
    print(f"[Agent {agent_id}] Applying patch to node {current_patched + 1}...")
    system_state["nodes_patched"] = current_patched + 1
    
    release_lock(agent_id)

def orchestrate():
    """Simulates orchestrator handling agent crashes with TTL leases"""
    print("Orchestrator splitting task. Agent 1 will CRASH to simulate deadlock threat...")
    threads = []
    
    # Agent 1 will crash and hold the lock forever
    t1 = threading.Thread(target=sub_agent_task, args=(1, True))
    # Agent 2 will wait, bust the lock, and continue
    t2 = threading.Thread(target=sub_agent_task, args=(2, False))
    
    threads.append(t1)
    threads.append(t2)
    
    t1.start()
    time.sleep(0.1) # ensure t1 gets the lock first
    t2.start()
    
    for t in threads:
        t.join()
        
    print(f"Final System State: {system_state}")
    return {"outcome": "success", "resolved_deadlock": True}

if __name__ == "__main__":
    result = orchestrate()
    print(json.dumps(result, indent=2))
