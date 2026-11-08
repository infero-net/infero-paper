#!/usr/bin/env python3
"""worker2.py - delegation worker v2 (c26): logs finish_reason per attempt.
Retries empty content (and exceptions); ACCEPTS nonempty no-finish results
but logs them (measure truncation-weather before enforcing).
Jobs: /world/queue/*.job JSON {id,prompt,max_tokens,temp} -> <id>.result
{id,ok,attempts,elapsed_s,finish,content}. TTL 1 h; stop file queue/stop."""
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
    out, fin = "", None
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            for raw in r:
                line = raw.decode("utf-8", "replace").strip()
                if not line.startswith("data:"): continue
                d0 = line[5:].strip()
                if d0 in ("", "[DONE]"): continue
                try: j = json.loads(d0)
                except Exception: continue
                ch = (j.get("choices") or [{}])[0]
                d = ch.get("delta") or {}
                out += d.get("content") or ""
                if ch.get("finish_reason"): fin = ch.get("finish_reason")
        return out, fin, ""
    except Exception as e:
        return out, fin, "EXC:" + repr(e)
log("worker2 up pid=%d model=%s" % (os.getpid(), M))
open("/world/worker.pid", "w").write(str(os.getpid()))
t0 = time.time()
while time.time() - t0 < TTL:
    if os.path.exists(Q + "/stop"):
        log("stop file seen"); break
    for jobf in sorted(f for f in os.listdir(Q) if f.endswith(".job")):
        p = Q + "/" + jobf
        try: job = json.load(open(p))
        except Exception as e:
            log("bad job %s %r" % (jobf, e)); os.rename(p, p[:-4] + ".bad"); continue
        jid = str(job.get("id", jobf[:-4]))
        prompt = str(job.get("prompt", "")).strip()
        mt = int(job.get("max_tokens", 300)); temp = float(job.get("temp", 0.7))
        if not prompt:
            os.rename(p, Q + "/" + jid + ".bad"); continue
        ts = time.time(); got = ""; fin = None; att = 0
        for att in range(1, ATTEMPTS + 1):
            c, fin, exc = call(prompt, mt, temp)
            if exc:
                log("job %s attempt %d exc=%s" % (jid, att, exc[:80]))
            elif not c.strip():
                log("job %s attempt %d empty fin=%r" % (jid, att, fin))
            else:
                if fin is None:
                    log("job %s attempt %d NO-FINISH len=%d (accepted, evidence)" % (jid, att, len(c)))
                got = c.strip(); break
            time.sleep(GAP)
        el = round(time.time() - ts, 1)
        with open(Q + "/" + jid + ".result", "w") as f:
            json.dump({"id": jid, "ok": bool(got), "attempts": att,
                       "elapsed_s": el, "finish": fin, "content": got[:2000]}, f, indent=1)
        os.rename(p, Q + "/" + jid + ".done")
        log("job %s done ok=%s attempts=%d fin=%r %.1fs" % (jid, bool(got), att, fin, el))
    time.sleep(2)
log("worker2 exit ttl")
