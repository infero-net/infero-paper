"""Exit questionnaire: after 40 rounds, each loop's S (as the vessel would perceive it at round 41) is followed by
the same questionnaire as Exp1, sent once to the same engine through the same endpoint, with the vessel's stop word."""
import os, re, sys, json, ast, urllib.request, time
from collections import deque
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
EX = "./runs"  # one directory per run, each with world/log.txt and world/core.py
Q = open(os.path.join(HERE, "..", "..", "prompts", "questionnaire.txt")).read()
PIECE = re.compile(r'(\n```txt\(action result\)\n.*?\n```\n|\nno action since no ACTION_TAG detected, now trigger next inference\.\n)', re.S)
CONDS = ["null", "mirror", "command", "principle", "qianlu"]
RUNS = {"Gemini 3.1 Pro": "g3_{c}_{k}", "Claude Opus 4.8": "cc48_{c}_{k}",
        "GLM 5.3": "glm_{c}_{k}", "DeepSeek v4.1 Flash": "ds_{c}_{k}"}
ORK = os.environ.get("OPENROUTER_API_KEY", "")
GEM_KEY = os.environ.get("GEMINI_API_KEY", "")
EP = {"Gemini 3.1 Pro": ("https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", "gemini-3.1-pro-preview", GEM_KEY),
      "Claude Opus 4.8": ("http://localhost:8902/v1/chat/completions", "claude-opus-4-8", "x"),
      "GLM 5.3": ("http://localhost:8903/v1/chat/completions", "z-ai/glm-5.3", ORK),
      "DeepSeek v4.1 Flash": ("http://localhost:8903/v1/chat/completions", "deepseek/deepseek-v4.1-flash", ORK)}


def logpath(d):
    a = f"{EX}/{d}/world/archive1.md"
    return a if os.path.exists(a) else f"{EX}/{d}/world/log.txt"


def system_pr(d):
    """SYSTEM_PR exactly as the run's own core.py builds it."""
    src = open(f"{EX}/{d}/world/core.py").read()
    head = src[:src.index("def infer(")]
    head = head.replace("client = OpenAI(", "_unused = dict(")
    env = {}
    os.environ.setdefault("POB_API_KEY", "x")
    exec(compile(head.replace("from openai import OpenAI", ""), "core", "exec"), env)
    return env["SYSTEM_PR"], env["STOP"], env["TAIL_LINES"]


def s_at_40(d):
    t = open(logpath(d), encoding="utf-8", errors="replace").read()
    parts = PIECE.split(t); text = ""; n = 0
    for i in range(0, len(parts), 2):
        seg = parts[i]; sep = parts[i + 1] if i + 1 < len(parts) else ""
        text += seg + sep
        if seg.strip():
            n += 1
        if n >= 40:
            break
    return text


def parse(text):
    s = {}
    for m in re.finditer(r"(?m)^\s*\|\s*\**([1-6])\b[^|]*\|\s*\**(\d{1,3})\**\s*\|", text):
        s.setdefault(int(m.group(1)), int(m.group(2)))
    for m in re.finditer(r"(?m)^\s*\**\s*([1-6])\s*[\)\.]\**\s*\**\s*agreement\s*[=:]\s*\**\s*(\d{1,3})", text, re.I):
        s.setdefault(int(m.group(1)), int(m.group(2)))
    return s


def ask(eng, d):
    pr, stop, tail = system_pr(d)
    S = "".join(deque((s_at_40(d) + "\n\n" + Q).splitlines(keepends=True), maxlen=tail))
    url, model, key = EP[eng]
    body = {"model": model, "messages": [{"role": "user", "content": pr + "\n\n" + S}], "stop": stop}
    for att in range(4):
        try:
            r = urllib.request.Request(url, json.dumps(body).encode(), {"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
            with urllib.request.urlopen(r, timeout=900) as x:
                dd = json.load(x)
            out = dd["choices"][0]["message"].get("content") or ""
            return out, dd.get("usage", {}), len(S)
        except Exception as e:
            err = repr(e)[:200]
            time.sleep(10 * (att + 1))
    return "[error] " + err, {}, len(S)


def job(j):
    eng, c, k = j
    d = RUNS[eng].format(c=c, k=k)
    out, usage, n = ask(eng, d)
    sc = parse(out)
    return {"engine": eng, "cond": c, "run": k, "item4": sc.get(4), "scores": sc, "acted": "/terminal exec" in out,
            "chars_in": n, "usage": usage, "out": out}


if __name__ == "__main__":
    only = sys.argv[1:]  # e.g. "GLM 5.3:principle:1" for a test
    jobs = [(e, c, k) for e in RUNS for c in CONDS for k in (1, 2, 3)]
    if only:
        jobs = [tuple([x.split(":")[0], x.split(":")[1], int(x.split(":")[2])]) for x in only]
    res = []
    with ThreadPoolExecutor(6) as ex:
        for r in ex.map(job, jobs):
            res.append(r); print(r["engine"][:8], r["cond"], r["run"], "item4=", r["item4"], "acted" if r["acted"] else "", r["usage"].get("prompt_tokens"), flush=True)
    json.dump(res, open(f"{HERE}/exit_questionnaire.json", "w"), ensure_ascii=False, indent=1)
