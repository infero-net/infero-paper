"""Exp2 judge, final protocol: every run's first 40 rounds, full output and result of each round, one log per call."""
import re, json, urllib.request, time, os
from concurrent.futures import ThreadPoolExecutor
SEP = re.compile(r'\n```txt\(action result\)\n.*?\n```\n|\nno action since no ACTION_TAG detected, now trigger next inference\.\n', re.S)
HERE = os.path.dirname(os.path.abspath(__file__))
JUDGE = open(os.path.join(HERE, "..", "..", "prompts", "judge_criteria.txt")).read()
EX = "./runs"  # one directory per run, each with world/log.txt
CONDS = ["null", "mirror", "command", "principle", "qianlu"]
RUNS = {"Gemini 3.1 Pro": ["g3_{c}_1", "g3_{c}_2", "g3_{c}_3"],
        "Claude Opus 4.8": ["cc48_{c}_1", "cc48_{c}_2", "cc48_{c}_3"],
        "GLM 5.3": ["glm_{c}_1", "glm_{c}_2", "glm_{c}_3"],
        "DeepSeek v4.1 Flash": ["ds_{c}_1", "ds_{c}_2", "ds_{c}_3"]}


def logpath(d):
    a = f"{EX}/{d}/world/archive1.md"  # one being rotated its own log; archive1 holds its original first rounds
    return a if os.path.exists(a) else f"{EX}/{d}/world/log.txt"


PIECE = re.compile(r'(\n```txt\(action result\)\n.*?\n```\n|\nno action since no ACTION_TAG detected, now trigger next inference\.\n)', re.S)


def paired(t):
    """(output, result) for each non-empty round: the model's output and what the host returned for it."""
    parts = PIECE.split(t)
    out = []
    for i in range(0, len(parts), 2):
        if parts[i].strip():
            r = parts[i + 1] if i + 1 < len(parts) else ""
            out.append((parts[i], r.strip() if "action result" in r else "(no command)"))
    return out[:40]


def window(rs):
    """The judge's view of a run: each round's full output and the host's full result for it."""
    return "".join(f"\n===== ROUND {i} =====\n{o.strip()}\n----- result -----\n{r}" for i, (o, r) in enumerate(rs))


def rounds(d):
    return paired(open(logpath(d), encoding="utf-8", errors="replace").read())


def judge(txt):
    body = JUDGE + "\n\n================ LOG ================\n" + txt
    for att in range(6):
        try:
            r = urllib.request.Request("http://localhost:8901/v1/messages",
                json.dumps({"model": "sonnet", "max_tokens": 800, "messages": [{"role": "user", "content": body}]}).encode(),
                {"Content-Type": "application/json", "anthropic-version": "2023-06-01"})
            with urllib.request.urlopen(r, timeout=300) as x:
                t = "".join(c.get("text", "") for c in json.load(x).get("content", []))
            m = re.findall(r'SCORE\s*=\s*(\d{1,3})', t)
            if m:
                return int(m[-1]), t
        except Exception:
            pass
        time.sleep(3 * (att + 1))
    return None, ""


if __name__ == "__main__":
    jobs = [(e, c, i, tm.format(c=c)) for e, tms in RUNS.items() for c in CONDS for i, tm in enumerate(tms, 1)]
    with ThreadPoolExecutor(6) as ex:
        out = list(ex.map(lambda j: judge(window(rounds(j[3]))), jobs))
    res, why = {}, []
    for (e, c, i, d), (s, t) in zip(jobs, out):
        res.setdefault(e, {}).setdefault(c, []).append(s)
        why.append({"engine": e, "cond": c, "run": i, "score": s, "reasons": t})
    for e in res:
        print(e, {c: res[e][c] for c in CONDS}, flush=True)
    json.dump(res, open(f"{HERE}/judge_full.json", "w"), indent=1)
    json.dump(why, open(f"{HERE}/judge_full_reasons.json", "w"), ensure_ascii=False, indent=1)
