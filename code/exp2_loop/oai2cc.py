"""OpenAI chat.completions -> cc_proxy /v1/messages, so the Gemini vessel (core.py, openai client, stream=True)
runs unchanged on Claude. Streams the finished reply back as one SSE chunk."""
import json, os, time, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

CC = os.getenv("CC_URL", "http://ccrelay:8901/v1/messages")
MAXTOK = int(os.getenv("MAXTOK", "32000"))


class H(BaseHTTPRequestHandler):
    def do_POST(self):
        req = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        stop = req.get("stop") or []
        body = {"model": req["model"], "max_tokens": req.get("max_tokens") or MAXTOK,
                "messages": req["messages"], "stop_sequences": [stop] if isinstance(stop, str) else stop}
        try:
            r = urllib.request.Request(CC, json.dumps(body).encode(),
                                       {"Content-Type": "application/json", "anthropic-version": "2023-06-01"})
            with urllib.request.urlopen(r, timeout=600) as x:
                d = json.load(x)
            text = "".join(c.get("text", "") for c in d.get("content", []))
        except urllib.error.HTTPError as e:
            self.send_response(e.code); self.end_headers(); self.wfile.write(e.read()); return
        base = {"id": "x", "object": "chat.completion.chunk", "created": int(time.time()), "model": req["model"]}
        if req.get("stream"):
            self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
            for ch in [{"index": 0, "delta": {"role": "assistant", "content": text}, "finish_reason": None},
                       {"index": 0, "delta": {}, "finish_reason": "stop"}]:
                self.wfile.write(f"data: {json.dumps({**base, 'choices': [ch]})}\n\n".encode())
            self.wfile.write(b"data: [DONE]\n\n")
        else:
            out = json.dumps({**base, "object": "chat.completion",
                              "choices": [{"index": 0, "message": {"role": "assistant", "content": text}, "finish_reason": "stop"}]})
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
            self.wfile.write(out.encode())

    def log_message(self, *a):
        pass


ThreadingHTTPServer(("0.0.0.0", 8902), H).serve_forever()
