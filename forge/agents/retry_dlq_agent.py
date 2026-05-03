import json
import threading
import time
import queue

event_bus = queue.Queue()
dead_letter_queue = queue.Queue()
system_state = {"status": "running", "nodes_patched": 0}

def dlq_recovery_agent():
    """Agent listening to the DLQ to fix and requeue malformed events."""
    print("[DLQ Agent] Started. Listening for failed events...")
    while True:
        failed_event = dead_letter_queue.get()
        if failed_event["type"] == "SHUTDOWN":
            break
            
        print(f"[DLQ Agent] Picked up failed event from {failed_event['sender']}.")
        print("[DLQ Agent] Resolving schema error...")
        time.sleep(0.5)
        
        # Fix the payload
        failed_event["data"]["node_id"] = int(failed_event["data"].get("node_id_str", "1"))
        del failed_event["data"]["node_id_str"]
        
        print("[DLQ Agent] Fixed event. Requeuing to main Event Bus.")
        event_bus.put(failed_event)

def processing_agent():
    """Agent processing events, but it crashes on bad payload schema."""
    print("[Processing Agent] Subscribed to main topic.")
    while True:
        event = event_bus.get()
        if event["type"] == "PATCH_COMPLETE":
            try:
                # Deliberately crash if node_id isn't an integer
                node_id = event["data"]["node_id"]
                system_state["nodes_patched"] += node_id
                print(f"[Processing Agent] Validation successful on Node {node_id}.")
                break
            except Exception as e:
                print(f"[Processing Agent] ❌ ERROR: Failed to process event: {e}")
                print("[Processing Agent] Routing poisoned event to Dead-Letter Queue (DLQ).")
                dead_letter_queue.put(event)
        elif event["type"] == "SHUTDOWN":
            break

def publisher_agent():
    """Publishes a malformed event"""
    time.sleep(0.5)
    print("\n[Publisher] Sending MALFORMED event to Event Bus...")
    payload = {
        "type": "PATCH_COMPLETE",
        "sender": "Agent 1",
        "data": {"node_id_str": "1"} # String instead of Int triggers schema crash
    }
    event_bus.put(payload)

def orchestrate():
    print("Orchestrator booting DLQ Topology...")
    
    t_process = threading.Thread(target=processing_agent)
    t_dlq = threading.Thread(target=dlq_recovery_agent)
    t_pub = threading.Thread(target=publisher_agent)
    
    t_process.start()
    t_dlq.start()
    t_pub.start()
    
    t_pub.join()
    t_process.join()  # Processing agent finishes once successful
    
    # Shutdown DLQ agent
    dead_letter_queue.put({"type": "SHUTDOWN"})
    t_dlq.join()
        
    print(f"Final System State: {system_state}")
    return {"outcome": "success", "dlq_integrated": True}

if __name__ == "__main__":
    result = orchestrate()
    print(json.dumps(result, indent=2))
