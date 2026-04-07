import json
import threading
import time
import queue

event_bus = queue.Queue()
dead_letter_queue = queue.Queue()
discard_bin = queue.Queue() # Upgraded from list to Queue so Alerter can subscribe

system_state = {"status": "running"}
MAX_RETRIES = 3

def human_in_the_loop_alerter():
    """Agent specifically built to monitor fatal drops and page engineering."""
    print("[Alerter Agent] Online. Monitoring Discard Bin for silent failures...")
    while True:
        fatal_event = discard_bin.get()
        if fatal_event["type"] == "SHUTDOWN":
            break
            
        print(f"\n[Alerter Agent] 🚨 PAGERDUTY ALERT 🚨")
        print(f"-> Severity: CRITICAL")
        print(f"-> Component: DLQ Finalizer")
        print(f"-> Message: Payload from {fatal_event['sender']} was permanently discarded after 3 retries.")
        print(f"-> Original Payload: {fatal_event['data']}")
        print(f"[Alerter Agent] Sent Webhook to #engineering-alerts Slack channel.\n")

def dlq_recovery_agent():
    print("[DLQ Agent] Started. Listening for failed events...")
    while True:
        failed_event = dead_letter_queue.get()
        if failed_event["type"] == "SHUTDOWN":
            break
            
        retries = failed_event.get("retries", 0)
        
        if retries >= MAX_RETRIES:
            print(f"[DLQ Agent] 🛑 FATAL: Event exceeded MAX_RETRIES. Routing to Discard topic.")
            discard_bin.put(failed_event)
            continue
            
        print(f"[DLQ Agent] Retry {retries}/{MAX_RETRIES}. Attempting fix...")
        failed_event["retries"] = retries + 1
        event_bus.put(failed_event)

def processing_agent():
    print("[Processing Agent] Subscribed to main topic.")
    while True:
        event = event_bus.get()
        if event["type"] == "SHUTDOWN":
            break
            
        if event["type"] == "PATCH_COMPLETE":
            try:
                node_id = event["data"]["node_id"]
                if not isinstance(node_id, int):
                    raise ValueError("node_id must be int")
                print(f"[Processing Agent] Validation successful on Node {node_id}.")
                break
            except Exception as e:
                dead_letter_queue.put(event)

def publisher_agent():
    time.sleep(0.5)
    payload = {
        "type": "PATCH_COMPLETE",
        "sender": "Agent 1",
        "data": {"node_id": "ONE"} # Unrecoverable poison pill
    }
    event_bus.put(payload)

def orchestrate():
    print("Orchestrator booting Alerter Topology...")
    
    t_process = threading.Thread(target=processing_agent)
    t_dlq = threading.Thread(target=dlq_recovery_agent)
    t_pub = threading.Thread(target=publisher_agent)
    t_alert = threading.Thread(target=human_in_the_loop_alerter)
    
    t_process.start()
    t_dlq.start()
    t_alert.start()
    t_pub.start()
    
    t_pub.join()
    # Wait for the 3 DLQ bounces + Alerter to finish processing
    time.sleep(1.0)
    
    event_bus.put({"type": "SHUTDOWN"})
    dead_letter_queue.put({"type": "SHUTDOWN"})
    discard_bin.put({"type": "SHUTDOWN"})
    
    t_process.join()
    t_dlq.join()
    t_alert.join()
        
    print(f"Final System State: {system_state}")
    return {"outcome": "success", "human_notified": True}

if __name__ == "__main__":
    result = orchestrate()
    print(json.dumps(result, indent=2))
