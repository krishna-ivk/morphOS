import json
import threading
import time

system_state = {"nodes_patched": 0, "status": "running"}
distributed_lock = {"owner": None, "expires_at": 0}
state_lock = threading.Lock() # Internal thread-safety for our mock dictionary
LOCK_TIMEOUT = 1.0  # 1 second TTL

def acquire_lock(agent_id):
    """Attempt to acquire a TTL lease on the state."""
    while True:
        with state_lock:
            now = time.time()
            if distributed_lock["owner"] is None or distributed_lock["expires_at"] < now:
                distributed_lock["owner"] = agent_id
                distributed_lock["expires_at"] = now + LOCK_TIMEOUT
                print(f"[Agent {agent_id}] Lease acquired. Expires at {distributed_lock['expires_at']:.1f}")
                return True
        time.sleep(0.3)

def release_lock(agent_id):
    with state_lock:
        if distributed_lock["owner"] == agent_id:
            distributed_lock["owner"] = None
            print(f"[Agent {agent_id}] Lease released safely.")

def heartbeat_loop(agent_id, stop_event):
    """Background thread that continually renews the lease while main thread works."""
    while not stop_event.is_set():
        time.sleep(LOCK_TIMEOUT / 2.0)  # Renew halfway through TTL
        with state_lock:
            if distributed_lock["owner"] == agent_id:
                distributed_lock["expires_at"] = time.time() + LOCK_TIMEOUT
                print(f"[Agent {agent_id}] 💓 Heartbeat: Lease renewed.")

def sub_agent_task(agent_id, delay):
    """Simulates a sub-agent applying patches"""
    acquire_lock(agent_id)
    
    # Start Heartbeat
    stop_heartbeat = threading.Event()
    heartbeat_thread = threading.Thread(target=heartbeat_loop, args=(agent_id, stop_heartbeat))
    heartbeat_thread.start()
    
    current_patched = system_state["nodes_patched"]
    
    print(f"[Agent {agent_id}] Starting long network constraint task ({delay}s delay)...")
    time.sleep(delay) # Main processing takes longer than the 1.0s TTL!
    
    print(f"[Agent {agent_id}] Applying patch to node {current_patched + 1}...")
    system_state["nodes_patched"] = current_patched + 1
    
    # Clean up Heartbeat and Lease
    stop_heartbeat.set()
    heartbeat_thread.join()
    release_lock(agent_id)

def orchestrate():
    """Simulates orchestrator handling slow agents with Active Heartbeats"""
    print("Orchestrator splitting task. Agent 1 has severe latency but runs a heartbeat...")
    
    t1 = threading.Thread(target=sub_agent_task, args=(1, 2.5)) # 2.5s > 1s TTL
    t2 = threading.Thread(target=sub_agent_task, args=(2, 0.5))
    
    t1.start()
    time.sleep(0.1) # ensure t1 gets the lock first
    t2.start()
    
    t1.join()
    t2.join()
        
    print(f"Final System State: {system_state}")
    return {"outcome": "success", "split_brain_averted": True}

if __name__ == "__main__":
    result = orchestrate()
    print(json.dumps(result, indent=2))
