import json

with open("feature_plan.json") as f:
    data = json.load(f)

tasks = []

for f in data["features"]:
    tasks.append({
        "task": f["name"],
        "description": f["description"]
    })

with open("tasks.json","w") as f:
    json.dump(tasks,f,indent=2)
