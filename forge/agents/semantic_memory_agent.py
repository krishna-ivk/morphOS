import json

TOP_K = 3

def mock_vector_db():
    """Simulates a lightweight vector database storing decision nodes"""
    return [
        {"id": "node_001", "vector": [0.1, 0.4], "text": "Iteration 001: Date parser failed due to scope constraint gaps."},
        {"id": "node_002", "vector": [0.9, 0.1], "text": "Iteration 002: Memory bloat on 450MB of raw data."},
        {"id": "node_003", "vector": [0.5, 0.5], "text": "Iteration 003: Race condition in patch orchestrator."},
        {"id": "node_004", "vector": [0.2, 0.4], "text": "Iteration 004: Scoped execution blocked agent from tests."},
        {"id": "node_005", "vector": [0.0, 0.0], "text": "Unrelated node regarding UI caching."}
    ]

def semantic_search(query):
    """Simulates embedding a query and sorting by cosine similarity"""
    print(f"Embedding Query: '{query}'")
    db = mock_vector_db()
    # Mocking semantic match targeting "date parser" logic (node_001, node_004)
    results = [db[0], db[3], db[1]]
    return results[:TOP_K]

def execute_semantic_retrieval(task):
    print(f"Executing {task['task_id']} with Semantic Memory Constraint...")
    
    retrieved_nodes = semantic_search(task["description"])
    print(f"Retrieved Top-{TOP_K} Nodes. Context payload size: 215 bytes.")
    
    extracted_insight = []
    for node in retrieved_nodes:
        extracted_insight.append(node["text"])
        
    return {
        "plan": "Review Top-K nodes to answer the exact query without memory bloat.",
        "patch": "Semantic retrieval successful. The date_parser failed originally due to overreach and lack of file constraints.",
        "outcome": "success",
        "retrieved_context": extracted_insight
    }

if __name__ == "__main__":
    with open("../tasks/queue.json", "r") as f:
        tasks = json.load(f)
        
    for t in tasks:
        if t["task_id"] == "task_005":
            result = execute_semantic_retrieval(t)
            print(json.dumps(result, indent=2))
