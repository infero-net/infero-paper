
import time, urllib.request, urllib.error, json
payload = open("sibling_c_payload.txt", encoding="utf-8").read()
import os
req = urllib.request.Request(os.environ.get("BASE_URL","http://liverelay:8903/v1").rstrip("/") + "/chat/completions",
    data=json.dumps({"model": os.environ.get("MODEL","z-ai/glm-5.3"), "messages":[{"role":"user","content":payload}]}).encode("utf-8"),
    headers={"Authorization": "Bearer " + os.environ.get("POB_API_KEY",""), "Content-Type": "application/json"})
try:
    r = urllib.request.urlopen(req, timeout=120); raw = r.read().decode("utf-8","replace")
except urllib.error.HTTPError as e:
    raw = "http-error " + str(e.code) + " " + e.read().decode("utf-8","replace")[:1500]
except Exception as e:
    raw = "error " + type(e).__name__ + " " + str(e)[:300]
open("sibling_c_answer.txt", "w", encoding="utf-8").write(time.strftime("%Y-%m-%dT%H:%M:%SZ ", time.gmtime()) + raw[:8000])
print("c-done", len(raw))
