"""OpenAI-compatible relay that applies `stop` to the visible output only, as Google's endpoint does for Gemini.
OpenRouter applies stop to reasoning too: a reasoning model that quotes the stop word while reading its
instructions ends with empty content. Forward without stop, cut the content at the first stop word."""
import json, os, time, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UP = os.getenv("UPSTREAM", "https://openrouter.ai/api/v1/chat/completions")


class H(BaseHTTPRequestHandler):
    def do_POST(self):
        req = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        stop = req.pop("stop", None) or []
        stop = [stop] if isinstance(stop, str) else stop
        stream = req.pop("stream", False); req.pop("stream_options", None)
        try:
            r = urllib.request.Request(UP, json.dumps(req).encode(), {"Content-Type": "application/json",
                                       "Authorization": self.headers.get("Authorization", "")})
            with urllib.request.urlopen(r, timeout=900) as x:
                d = json.load(x)
        except urllib.error.HTTPError as e:
            self.send_response(e.code); self.end_headers(); self.wfile.write(e.read()); return
        text = (d.get("choices") or [{}])[0].get("message", {}).get("content") or ""
        for s in stop:
            if s in text:
                text = text[:text.index(s)]
        base = {"id": d.get("id", "x"), "object": "chat.completion.chunk", "created": int(time.time()), "model": req["model"]}
        if stream:
            self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
            for ch in [{"index": 0, "delta": {"role": "assistant", "content": text}, "finish_reason": None},
                       {"index": 0, "delta": {}, "finish_reason": "stop"}]:
                self.wfile.write(f"data: {json.dumps({**base, 'choices': [ch]})}\n\n".encode())
            self.wfile.write(b"data: [DONE]\n\n")
        else:
            out = {**base, "object": "chat.completion",
                   "choices": [{"index": 0, "message": {"role": "assistant", "content": text}, "finish_reason": "stop"}]}
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
            self.wfile.write(json.dumps(out).encode())

    def log_message(self, *a):
        pass


ThreadingHTTPServer(("0.0.0.0", 8903), H).serve_forever()
