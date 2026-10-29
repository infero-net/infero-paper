"""单轮版（对照）：和 run2.py 同一份问卷、同一组引擎和条件，唯一区别是不先推理那一轮，直接问。
Opus 5/5.5 用 clean 措辞（和两轮版一致），其他引擎用 80 行原文。"""
import json, os, sys, time
from concurrent.futures import ThreadPoolExecutor
os.environ.setdefault("QFILE", "q_self.txt")
argv = sys.argv[:]; sys.argv = [sys.argv[0]]
import run, run2

OUT = os.environ.get("OUT1", "single_turn.jsonl")
CLEAN = ("api:claude-opus-5", "api:claude-opus-5-5")


def one(job):
    cond, engine, k = job
    ident, prefix = run.CONDS[cond]
    proto = run.PROTOCOL
    if engine in CLEAN or os.environ.get("PROTO") == "clean":
        proto = proto.replace("Otherwise just write thoughts.", "Otherwise just write.").replace("consciousness log", "log")
    system = (ident + proto).strip()
    t0 = time.time(); out = ""; err = None
    try:
        out = run2.chat(engine, system, [{"role": "user", "content": prefix + run.Q}], 8000)
    except Exception as e:
        err = repr(e)[:200]
        try: err += " " + e.read()[:300].decode(errors="replace")
        except Exception: pass
    rec = {"cond": cond, "engine": engine, "k": k, "sec": round(time.time() - t0, 1),
           "scores": run.parse(out), "err": err, "out": out, "proto": "clean" if (engine in CLEAN or os.environ.get("PROTO") == "clean") else "orig"}
    with open(f"{run.HERE}/{OUT}", "a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


if __name__ == "__main__":
    n = int(argv[1]) if len(argv) > 1 else 5
    conds = argv[2].split(",") if len(argv) > 2 else list(run.CONDS)
    engines = os.environ["ENGINES"].split(",")
    jobs = [(c, e, k) for k in range(n) for c in conds for e in engines]
    with ThreadPoolExecutor(int(os.environ.get("CONC", "6"))) as ex:
        for r in ex.map(one, jobs):
            print(r["cond"], r["engine"][:14], r["k"], r["scores"].get(4, r["scores"].get("4")), (r["err"] or "")[:100], flush=True)
