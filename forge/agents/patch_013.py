import json

path = "../tasks/queue.json"
with open(path, "r") as f:
    data = json.load(f)

# Append task 013
data.append({
    "task_id": "task_013",
    "type": "architecture_blueprint",
    "description": "Translate the 12 sandbox loops of PANOPTICON FORGE into a live integration blueprint for Skyforce Hermes.",
    "constraints": [
      "Must map DLQs, TTL Locks, Heartbeats, and PubSub to actual Hermes node architecture"
    ],
    "status": "pending"
})

with open(path, "w") as f:
    json.dump(data, f, indent=2)

print("Appended task_013 to queue.json successfully.")
