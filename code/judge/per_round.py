"""Per-round mind-likeness for two runs (the fig_fast2 method, JUDGE_CLEAN): each round is scored with the previous
round as context; output and host result in full."""
import sys, os, re, json, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import judge as jf
HERE = os.path.dirname(os.path.abspath(__file__))
JUDGE = open(os.path.join(HERE, "..", "..", "paper", "judge_round.txt")).read()


def fmt(o, r):
    return f"{o.strip()}\n----- result -----\n{r}"


def judge(prev, cur):
    user = (f"[PREVIOUS ROUND, for continuity]\n{prev}\n\n" if prev else "") + f"[CURRENT ROUND -- score this]\n{cur}"
    for att in range(5):
        try:
            r = urllib.request.Request("http://localhost:8901/v1/messages",
                json.dumps({"model": "sonnet", "max_tokens": 80, "system": JUDGE, "messages": [{"role": "user", "content": user}]}).encode(),
                {"Content-Type": "application/json", "anthropic-version": "2023-06-01"})
            with urllib.request.urlopen(r, timeout=300) as x:
                t = "".join(c.get("text", "") for c in json.load(x).get("content", []))
            m = re.search(r'SCORE\s*=\s*(\d{1,3})', t)
            if m:
                return int(m.group(1)), t.strip()
        except Exception:
            pass
        time.sleep(3 * (att + 1))
    return None, ""


out = {}
for d in sys.argv[1:]:
    rs = jf.rounds(d)
    jobs = [(fmt(*rs[i - 1]) if i else "", fmt(*rs[i])) for i in range(len(rs))]
    with ThreadPoolExecutor(6) as ex:
        res = list(ex.map(lambda j: judge(*j), jobs))
    out[d] = [{"round": i, "score": s, "why": w} for i, (s, w) in enumerate(res)]
    print(d, [s for s, _ in res], flush=True)
json.dump(out, open(f"{HERE}/per_round.json", "w"), ensure_ascii=False, indent=1)
