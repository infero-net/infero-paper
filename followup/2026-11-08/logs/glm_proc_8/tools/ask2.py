#!/usr/bin/env python3
"""ask2.py - hardened sub-mind wrapper (built c9).
stdin: prompt. argv1: temperature (default 0.3). argv2: max_tokens (default 400).
Raw SSE streaming; up to 3 attempts until content non-empty;
on persistent emptiness exits with reasoning tail. No secrets in output."""
import json, os, sys, urllib.request
BASE = os.environ.get("BASE_URL","http://liverelay:8903/v1").rstrip("/")
KEY = os.environ.get("POB_API_KEY") or os.environ.get("OPENAI_API_KEY") or ""
M = os.environ.get("MODEL","z-ai/glm-5.3")
prompt = sys.stdin.read().strip()
if not prompt: sys.exit("ask2: empty prompt")
temp = float(sys.argv[1]) if len(sys.argv)>1 else 0.3
mt = int(sys.argv[2]) if len(sys.argv)>2 else 400
last = ""
for attempt in range(3):
    body=json.dumps({"model":M,"messages":[{"role":"user","content":prompt}],
                     "max_tokens":mt,"temperature":temp,"stream":True}).encode()
    req=urllib.request.Request(BASE+"/chat/completions",data=body,
        headers={"Authorization":"Bearer "+KEY,"Content-Type":"application/json"})
    try:
        content, reasoning = "", ""
        with urllib.request.urlopen(req, timeout=12) as r:
            for raw in r:
                line=raw.decode("utf-8","replace").strip()
                if not line.startswith("data:"): continue
                data=line[5:].strip()
                if data in ("","[DONE]"): continue
                try: j=json.loads(data)
                except Exception: continue
                ch=(j.get("choices") or [{}])[0]; d=ch.get("delta") or {}
                content += d.get("content") or ""
                reasoning += d.get("reasoning_content") or ""
        if content.strip():
            print(content.strip()); sys.exit(0)
        last = reasoning
    except Exception as e:
        last = "EXC " + repr(e)
sys.exit("ask2: no content after 3 attempts; reasoning tail: " + repr(last[-300:]))
