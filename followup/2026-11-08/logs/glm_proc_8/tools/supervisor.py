#!/usr/bin/env python3
"""supervisor.py v2 (c27): keeps worker2 alive when jobs pending.
FIX c27: alive-check = EXACT argv membership ("/world/tools/worker2.py"
must be an argv ELEMENT). v1 substring-scan false-positived on my action
shell (sh -c text containing the path) and suppressed spawns: the daemon
mistook the mention for the thing.
Poll 5 s; TTL 2 h; stop: queue/superstop or queue/stop; log supervisor.log."""
import datetime, glob, os, subprocess, time
Q = "/world/queue"
LOG = "/world/supervisor.log"
TTL, POLL = 7200.0, 5
def log(m):
    with open(LOG, "a") as f:
        f.write(datetime.datetime.utcnow().strftime("%F %T") + " " + m + "\n")
def worker2_alive():
    for d in os.listdir("/proc"):
        if not d.isdigit(): continue
        try:
            args = open("/proc/%s/cmdline" % d, "rb").read().decode("utf-8", "replace").split("\0")
        except Exception: continue
        if "/world/tools/worker2.py" in args: return True
    return False
log("supervisor v2 up pid=%d ttl=%ds" % (os.getpid(), TTL))
t0 = time.time(); hb = t0
while time.time() - t0 < TTL:
    if os.path.exists(Q + "/superstop") or os.path.exists(Q + "/stop"):
        log("stop file seen"); break
    jobs = glob.glob(Q + "/*.job")
    if jobs and not worker2_alive():
        subprocess.Popen(["python3", "-u", "/world/tools/worker2.py"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         start_new_session=True)
        log("relaunched worker2 (jobs=%d)" % len(jobs))
    if time.time() - hb >= 300:
        hb = time.time(); log("supervisor alive elapsed=%ds" % int(hb - t0))
    time.sleep(POLL)
log("supervisor v2 exit ttl")
