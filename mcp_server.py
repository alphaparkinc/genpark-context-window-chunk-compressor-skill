import sys
import json
from client import ContextChunkCompressor

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-context-window-chunk-compressor-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "compress_context_window",
                        "description": "Compress long context text to retain query-relevant sentences within budget",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "context_text": {"type": "string", "description": "Large source text context"},
                                "query": {"type": "string", "description": "Target query for relevance focus"},
                                "max_chars": {"type": "integer", "default": 500}
                            },
                            "required": ["context_text", "query"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "compress_context_window":
            ctx = args.get("context_text", "")
            q = args.get("query", "")
            budget = args.get("max_chars", 500)
            res = ContextChunkCompressor.compress(ctx, q, budget)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps({"compressed_text": res, "original_len": len(ctx), "compressed_len": len(res)})}]
                }
            }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
