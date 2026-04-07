import json
import threading
import time
import queue

# Simulate an Event Bus (e.g., Redis PubSub or Kafka)
event_bus = queue.Queue()
system_state = {"status": "running", "nodes_patched": 0}

def agent_2_subscriber():
    """Agent 2 subscribes to the event bus waiting for the 'PATCH_COMPLETE' signal."""
    print("[Agent 2] Subscribed to topic: 'system_events'. Waiting for signal...")
    while True:
        event = event_bus.get()
        if event["type"] == "PATCH_COMPLETE":
            print(f"[Agent 2] Received PATCH_COMPLETE from {event['sender']}.")
            print(f"[Agent 2] Running validation on Node {event['data']['node_id']}...")
            time.sleep(0.5)
            print(f"[Agent 2] Validation successful. Task pipeline complete.")
            break
        elif event["type"] == "SHUTDOWN":
            break

def agent_1_publisher():
    """Agent 1 performs the work and then publishes a completion event."""
    print("[Agent 1] Applying patch to Node 1...")
    time.sleep(1.0)
    system_state["nodes_patched"] = 1
    
    # Broadcast to the Event Bus
    payload = {
        "type": "PATCH_COMPLETE",
        "sender": "Agent 1",
        "data": {"node_id": 1}
    }
    print(f"[Agent 1] Patch applied. Publishing event to Event Bus -> {payload['type']}")
    event_bus.put(payload)

def orchestrate():
    """Simulates orchestrator booting agents connected via PubSub instead of Locks."""
    print("Orchestrator booting A2A Event Bus topology...")
    
    t2 = threading.Thread(target=agent_2_subscriber)
    t1 = threading.Thread(target=agent_1_publisher)
    
    t2.start()
    time.sleep(0.1) # Let subscriber initialize
    t1.start()
    
    t1.join()
    t2.join()
        
    print(f"Final System State: {system_state}")
    return {"outcome": "success", "event_bus_active": True}

if __name__ == "__main__":
    result = orchestrate()
    print(json.dumps(result, indent=2))
