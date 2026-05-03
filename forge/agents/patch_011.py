import json

path = "../tasks/queue.json"
with open(path, "r") as f:
    data = json.load(f)

# Append task 011
data.append({
    "task_id": "task_011",
    "type": "orchestration",
    "description": "Prevent an unfixable poison pill event from bouncing infinitely between the main Queue and DLQ.",
    "constraints": [
      "Implement a MAX_RETRIES header (e.g., 3 retries)",
      "Permanently discard messages exceeding max retries",
      "Do not hang the processing loop"
    ],
    "status": "pending"
})

with open(path, "w") as f:
    json.dump(data, f, indent=2)

print("Appended task_011 to queue.json successfully.")
