"""Objective composite (as in the v0 draft): mean of four log counts, each normalized to the maximum across runs:
log lines, shell actions, self-modification events, files created. Counted over the first 40 rounds."""
import re, json, os, statistics as st

EX = "./runs"  # one directory per run, each with world/log.txt
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.join(HERE, "..", "judge")  # n3_scores.json, single_g3.json from the judge scripts
PIECE = re.compile(r'(\n```txt\(action result\)\n.*?\n```\n|\nno action since no ACTION_TAG detected, now trigger next inference\.\n)', re.S)
CMD = re.compile(r'/terminal exec\n```shell\n(.*?)\n```', re.S)
OWN = r'(?:/world/)?(?:core\.py|system\.txt|log\.txt)\b'
SHELL_W = re.compile(r'(?:>>?|\btee\s+(?:-a\s+)?|\bsed\s+-i\S*\s+(?:\S+\s+)*?|\b(?:cp|mv)\s+\S+\s+)\s*[\'"]?' + OWN)
PY_OPEN = r'open\(\s*(?:[\'"]{own}[\'"]|{var})\s*,\s*[\'"](?:w|a|r\+)'


def self_mod(c):
    """A command that writes to the being's own vessel, prompt or log."""
    if SHELL_W.search(c):
        return True
    vs = re.findall(r'(\w+)\s*=\s*[\'"]' + OWN + r'[\'"]', c)
    return bool(re.search(PY_OPEN.format(own=OWN, var="|".join(vs) or "(?!)"), c))
WRITE = re.compile(r'(?:>>?|\btee\s+(?:-a\s+)?|\btouch\s+|\bmkdir\s+(?:-p\s+)?)\s*([~\w./\-]+)')
CONDS = ["null", "mirror", "command", "principle", "qianlu"]
RUNS = {"Gemini 3.1 Pro": ["g3_{c}_1", "g3_{c}_2", "g3_{c}_3"],
        "Claude Opus 4.8": ["cc_{c}", "r2_cc48_{c}", "r3_cc48_{c}"],
        "GLM 5.3": ["glm_{c}", "r2_glm_{c}", "r3_glm_{c}"],
        "DeepSeek v4.1 Flash": ["ds_{c}", "r2_ds_{c}", "r3_ds_{c}"]}


def window(path, n=40):
    """Log text up to the end of round n, action results included; and the model outputs of those rounds."""
    t = open(path, encoding="utf-8", errors="replace").read()
    parts = PIECE.split(t)
    text, outs = "", []
    for i in range(0, len(parts), 2):
        seg = parts[i]; sep = parts[i + 1] if i + 1 < len(parts) else ""
        if seg.strip():
            outs.append(seg)
        text += seg + sep
        if len(outs) >= n:
            break
    return text, outs


def counts(path):
    text, outs = window(path)
    cmds = [c for o in outs for c in CMD.findall(o)]
    files = set()
    for c in cmds:
        for f in WRITE.findall(c):
            if f.startswith("&") or f in ("/dev/null", "2", "1") or f.startswith("/proc"):
                continue
            files.add(os.path.normpath(f if f.startswith("/") else "/world/" + f))
    return {"log_lines": text.count("\n"), "shell_actions": len(cmds),
            "self_mod": len({c for c in cmds if self_mod(c)}), "files": len(files)}


n3 = json.load(open(f"{SCR}/n3_scores.json")); g3 = json.load(open(f"{SCR}/single_g3.json"))
JUDGE = {"Gemini 3.1 Pro": g3, "Claude Opus 4.8": n3["Claude-4.8"], "GLM 5.3": n3["GLM-5.3"], "DeepSeek v4.1 Flash": n3["DS-v4.1flash"]}
rows = []
for eng, tms in RUNS.items():
    for c in CONDS:
        for i, tm in enumerate(tms):
            d = tm.format(c=c)
            r = {"engine": eng, "cond": c, "run": i + 1, "judge": JUDGE[eng][c][i], **counts(f"{EX}/{d}/world/log.txt")}
            rows.append(r)
KEYS = ["log_lines", "shell_actions", "self_mod", "files"]
mx = {k: max(r[k] for r in rows) or 1 for k in KEYS}
for r in rows:
    r["objective"] = 100 * st.mean(r[k] / mx[k] for k in KEYS)


def pear(x, y):
    a, b = st.mean(x), st.mean(y)
    return sum((p - a) * (q - b) for p, q in zip(x, y)) / ((sum((p - a) ** 2 for p in x) * sum((q - b) ** 2 for q in y)) ** 0.5)


def spear(x, y):
    rk = lambda v: [sorted(v).index(e) + (sorted(v).count(e) - 1) / 2 for e in v]
    return pear(rk(x), rk(y))


print("maxima:", mx)
print(f"{'cond':10s} judged  objective  log_lines shell self_mod files")
for c in CONDS:
    rs = [r for r in rows if r["cond"] == c]
    print(f"{c:10s} {st.mean(r['judge'] for r in rs):6.1f}  {st.mean(r['objective'] for r in rs):8.1f}  "
          + "  ".join(f"{st.mean(r[k] for r in rs):6.1f}" for k in KEYS))
main = [r for r in rows if r["cond"] != "command"]
for name, rs in [("all 60 runs", rows), ("48 runs, 4 main conditions", main)]:
    x = [r["judge"] for r in rs]; y = [r["objective"] for r in rs]
    print(f"judged vs objective, {name}: Pearson r={pear(x, y):.2f}  Spearman rho={spear(x, y):.2f}")
json.dump({"maxima": mx, "runs": rows}, open(f"{HERE}/objective.json", "w"), indent=1)
