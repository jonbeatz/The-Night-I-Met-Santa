import sys
import os
import argparse
import json

def get_memory_instance():
    from mem0 import Memory
    
    # Ensure local directory exists in the JonBeatz personal profile
    user_home = os.path.expanduser("~")
    mem0_dir = os.path.join(user_home, ".mem0")
    os.makedirs(mem0_dir, exist_ok=True)
    
    config = {
        "vector_store": {
            "provider": "qdrant",
            "config": {
                "collection_name": "the-night-i-met-santa_memories",
                "path": os.path.join(mem0_dir, "qdrant_the-night-i-met-santa"),
                "embedding_model_dims": 384,
            }
        },
        "llm": {
            "provider": "lmstudio",
            "config": {
                "model": "qwen3-4b-instruct-2507",
                "lmstudio_base_url": "http://127.0.0.1:1234/v1",
                "temperature": 0.1,
                "max_tokens": 512,
                "lmstudio_response_format": {"type": "json_schema", "json_schema": {"type": "object", "schema": {}}}
            }
        },
        "embedder": {
            "provider": "huggingface",
            "config": {
                "model": "multi-qa-MiniLM-L6-cos-v1"
            }
        }
    }
    return Memory.from_config(config)

def main():
    parser = argparse.ArgumentParser(description="JonBeatz Personal Mem0 Integration layer")
    parser.add_argument("--action", choices=["add", "search", "list", "delete", "get_all"], required=True, help="Action to perform")
    parser.add_argument("--text", help="Text to add (required for add action)")
    parser.add_argument("--query", help="Query to search (required for search action)")
    parser.add_argument("--id", help="Memory ID to delete (required for delete action)")
    args = parser.parse_args()
    
    # Simple check for LM Studio readiness when adding or searching
    if args.action in ["add", "search"]:
        import urllib.request
        try:
            urllib.request.urlopen("http://127.0.0.1:1234/v1/models", timeout=2)
        except Exception:
            print("[J.A.R.V.I.S. Warning] Local LM Studio endpoint (http://127.0.0.1:1234/v1) is not online. Please make sure LM Studio is running and local server is started on port 1234!")
            sys.exit(1)
            
        # Check if a model is loaded via lms ps
        import subprocess
        try:
            res = subprocess.run(["lms", "ps"], capture_output=True, text=True)
            if "No models are currently loaded" in res.stdout or not res.stdout.strip():
                print("[J.A.R.V.I.S. Warning] No local LLM models are currently loaded in LM Studio. Please load a model first.")
                sys.exit(1)
        except Exception:
            pass
        
    try:
        m = get_memory_instance()
        if args.action == "add":
            if not args.text:
                print(json.dumps({"success": False, "error": "--text is required for add action"}))
                sys.exit(1)
            # Add memory to personal collection
            res = m.add(args.text, user_id="jonbeatz_personal")
            print(json.dumps({"success": True, "data": res}))
            
        elif args.action == "search":
            if not args.query:
                print(json.dumps({"success": False, "error": "--query is required for search action"}))
                sys.exit(1)
            # Search memory in personal collection
            res = m.search(args.query, filters={"user_id": "jonbeatz_personal"})
            print(json.dumps({"success": True, "data": res}))

        elif args.action == "list" or args.action == "get_all":
            # List all memories for personal user
            res = m.get_all(filters={"user_id": "jonbeatz_personal"})
            print(json.dumps({"success": True, "data": res}))

        elif args.action == "delete":
            if not args.id:
                print(json.dumps({"success": False, "error": "--id is required for delete action"}))
                sys.exit(1)
            # Delete memory by ID
            res = m.delete(args.id)
            print(json.dumps({"success": True, "data": res}))
            
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
