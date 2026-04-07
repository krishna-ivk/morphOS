import json
import threading
import time
import queue

event_bus = queue.Queue()
dead_letter_queue = queue.Queue()
discard_bin = []

system_state = {"status": "running", "nodes_patched": 0}
MAX_RETRIES = 3

def dlq_recovery_agent():
    """Agent listening to the DLQ to fix and requeue events OR discard them."""
    print("[DLQ Agent] Started. Listening for failed events...")
    while True:
        failed_event = dead_letter_queue.get()
        if failed_event["type"] == "SHUTDOWN":
            break
            
        retries = failed_event.get("retries", 0)
        
        if retries >= MAX_RETRIES:
            print(f"[DLQ Agent] 🛑 FATAL: Event exceeded MAX_RETRIES ({MAX_RETRIES}).")
            print("[DLQ Agent] Permanently routing to Discard Bin.")
            discard_bin.append(failed_event)
            continue
            
        print(f"[DLQ Agent] Picked up failed event (Retry {retries}/{MAX_RETRIES}).")
        time.sleep(0.5)
        
        # DLQ Agent tries to fix it but fails to properly cast node_id_float to int
        # It just re-nests it, meaning it will still fail!
        print("[DLQ Agent] Attempting to fix schema constraint...")
        failed_event["retries"] = retries + 1
        
        print("[DLQ Agent] Requeuing to main Event Bus.")
        event_bus.put(failed_event)

def processing_agent():
    """Agent processing events, crashing on bad schema."""
    print("[Processing Agent] Subscribed to main topic.")
    while True:
        event = event_bus.get()
        if event["type"] == "SHUTDOWN":
            break
            
        if event["type"] == "PATCH_COMPLETE":
            try:
                # Expects 'node_id' to be present and strictly an integer
                node_id = event["data"]["node_id"]
                if not isinstance(node_id, int):
                    raise ValueError(f"node_id must be int, got {type(node_id)}")
                    
                system_state["nodes_patched"] += node_id
                print(f"[Processing Agent] Validation successful on Node {node_id}.")
                break
            except Exception as e:
                print(f"[Processing Agent] ❌ ERROR: Failed to process event: {e}")
                print("[Processing Agent] Routing poisoned event to Dead-Letter Queue (DLQ).")
                dead_letter_queue.put(event)

def publisher_agent():
    time.sleep(0.5)
    print("\n[Publisher] Sending UNFIXABLE MALFORMED event to Event Bus...")
    payload = {
        "type": "PATCH_COMPLETE",
        "sender": "Agent 1",
        "data": {"node_id": "ONE"} # String text "ONE" cannot be naively cast to int by DLQ
    }
    event_bus.put(payload)

def orchestrate():
    print("Orchestrator booting DLQ Max-Retry Topology...")
    
    t_process = threading.Thread(target=processing_agent)
    t_dlq = threading.Thread(target=dlq_recovery_agent)
    t_pub = threading.Thread(target=publisher_agent)
    
    t_process.start()
    t_dlq.start()
    t_pub.start()
    
    t_pub.join()
    # To prevent actual infinite hanging in the test, we sleep and cleanly shutdown
    time.sleep(4.0)
    
    event_bus.put({"type": "SHUTDOWN"})
    dead_letter_queue.put({"type": "SHUTDOWN"})
    
    t_process.join()
    t_dlq.join()
        
    print(f"\nFinal System State: {system_state}")
    print(f"Discard Bin Count: {len(discard_bin)}")
    
    if len(discard_bin) > 0:
        return {"outcome": "success", "poison_pill_discarded": True}
    return {"outcome": "failed", "reason": "Infinite loop detected."}

if __name__ == "__main__":
    result = orchestrate()
    print(json.dumps(result, indent=2))
