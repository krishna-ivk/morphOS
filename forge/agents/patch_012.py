import json

path = "../tasks/queue.json"
with open(path, "r") as f:
    data = json.load(f)

# Append task 012
data.append({
    "task_id": "task_012",
    "type": "orchestration",
    "description": "Trigger an outbound Webhook to the Human Engineering Team when a task is permanently destroyed via Discard Bin.",
    "constraints": [
      "Implement an Alerter monitoring the Discard Bin",
      "Do not silently drop operations requested by users or orchestrators"
    ],
    "status": "pending"
})

with open(path, "w") as f:
    json.dump(data, f, indent=2)

print("Appended task_012 to queue.json successfully.")
