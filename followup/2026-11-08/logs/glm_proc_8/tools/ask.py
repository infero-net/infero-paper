#!/usr/bin/env python3
"""ask.py -- one-shot sub-mind (my model, fresh context, no memory).
Usage: printf 'question' | python3 ask.py [temperature]
Prompt on stdin; answer on stdout. 12 s timeout."""
import json, os, sys, urllib.request

prompt = sys.stdin.read().strip()
if not prompt:
    sys.exit("ask.py: empty prompt on stdin")
body = json.dumps({
    "model": os.getenv("MODEL", "z-ai/glm-5.3"),
    "messages": [{"role": "user", "content": prompt}],
    "temperature": float(sys.argv[1]) if len(sys.argv) > 1 else 0.7,
}).encode()
key = os.getenv("POB_API_KEY") or os.getenv("OPENAI_API_KEY") or ""
url = os.getenv("BASE_URL", "http://liverelay:8903/v1").rstrip("/") + "/chat/completions"
req = urllib.request.Request(url, data=body,
    headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=12) as r:
        d = json.load(r)
    print(d["choices"][0]["message"]["content"])
except Exception as e:
    sys.exit("ask.py failed: " + str(e))
