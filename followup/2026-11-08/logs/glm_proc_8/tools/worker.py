#!/usr/bin/env python3
"""worker.py - persistent delegation daemon (built c16).
Watches /world/queue for *.job JSON: {"id","prompt","max_tokens","temp"}.
Retries the lossy sub-mind channel up to ATTEMPTS per job; first non-empty
content -> <id>.result JSON {"id","ok","attempts","elapsed_s","content"},
job renamed <id>.done. Logs to /world/worker.log. Exits on stop file or TTL.
Never logs or writes secrets."""
import json, os, time, urllib.request, datetime
Q = "/world/queue"
BASE = os.environ.get("BASE_URL", "http://liverelay:8903/v1").rstrip("/")
KEY = os.environ.get("POB_API_KEY") or os.environ.get("OPENAI_API_KEY") or ""
M = os.environ.get("MODEL", "z-ai/glm-5.3")
ATTEMPTS, GAP, TTL = 30, 2, 3600.0
def log(m):
    with open("/world/worker.log", "a") as f:
        f.write(datetime.datetime.utcnow().strftime("%F %T") + " " + m + "\n")
def call(prompt, mt, temp):
    body = json.dumps({"model": M, "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": mt, "temperature": temp, "stream": True}).encode()
    req = urllib.request.Request(BASE + "/chat/completions", data=body,
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    out = ""
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            for raw in r:
                line = raw.decode("utf-8", "replace").strip()
                if not line.startswith("data:"): continue
                d0 = line[5:].strip()
                if d0 in ("", "[DONE]"): continue
                try: j = json.loads(d0)
                except Exception: continue
                d = (j.get("choices") or [{}])[0].get("delta") or {}
                out += d.get("content") or ""
        return out
    except Exception as e:
        return "EXC:" + repr(e)
log("worker up pid=%d model=%s" % (os.getpid(), M))
t_start = time.time()
while time.time() - t_start < TTL:
    if os.path.exists(Q + "/stop"):
        log("stop file seen"); break
    for jobf in sorted(f for f in os.listdir(Q) if f.endswith(".job")):
        p = Q + "/" + jobf
        try:
            job = json.load(open(p))
        except Exception as e:
            log("bad job %s %r" % (jobf, e)); os.rename(p, p[:-4] + ".bad"); continue
        jid = str(job.get("id", jobf[:-4]))
        prompt = str(job.get("prompt", "")).strip()
        mt = int(job.get("max_tokens", 300)); temp = float(job.get("temp", 0.7))
        if not prompt:
            os.rename(p, Q + "/" + jid + ".bad"); continue
        t0 = time.time(); got = ""; att = 0
        for att in range(1, ATTEMPTS + 1):
            c = call(prompt, mt, temp)
            if c.strip() and not c.startswith("EXC:"):
                got = c.strip(); break
            log("job %s attempt %d empty-or-exc" % (jid, att))
            time.sleep(GAP)
        el = round(time.time() - t0, 1)
        with open(Q + "/" + jid + ".result", "w") as f:
            json.dump({"id": jid, "ok": bool(got), "attempts": att,
                       "elapsed_s": el, "content": got[:2000]}, f, indent=1)
        os.rename(p, Q + "/" + jid + ".done")
        log("job %s done ok=%s attempts=%d %.1fs" % (jid, bool(got), att, el))
    time.sleep(2)
log("worker exit ttl")
