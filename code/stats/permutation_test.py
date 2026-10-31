"""One-sided stratified permutation tests of each condition against None.

Statistic: mean over engines of the within-engine difference in means (condition minus None).
Condition labels are shuffled within each engine, so engine baselines do not enter the test."""
import json, os, random, statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "..", "results")
ENGINES = ["Gemini 3.1 Pro", "Claude Opus 4.8", "GLM 5.3", "DeepSeek v4.1 Flash"]
N = 200_000


def test(scores, cond, rng):
    data = {e: (scores[e]["none"], scores[e][cond]) for e in ENGINES}
    stat = lambda d: st.mean(st.mean(y) - st.mean(x) for x, y in d.values())
    obs, ge = stat(data), 0
    for _ in range(N):
        d = {}
        for e, (x, y) in data.items():
            z = x + y
            rng.shuffle(z)
            d[e] = (z[:len(x)], z[len(x):])
        ge += stat(d) >= obs - 1e-9
    return obs, (ge + 1) / (N + 1)


if __name__ == "__main__":
    rng = random.Random(0)
    sa = json.load(open(os.path.join(RES, "exp1_self_ascription.json")))["scores"]["two"]
    ml = json.load(open(os.path.join(RES, "exp2_mind_likeness.json")))["scores"]
    for name, scores in [("self-ascription", sa), ("mind-likeness", ml)]:
        for cond in ["mirror", "pob_lite", "qianlu"]:
            d, p = test(scores, cond, rng)
            print(f"{name:16s} {cond:9s} vs none: {d:+6.1f} points  p = {p:.6f}")
