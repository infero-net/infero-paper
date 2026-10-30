"""两轮版：先发条件 prompt，让模型自然推理一轮（B1），再把问卷作为下一条消息发过去。"""
import json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
os.environ.setdefault("QFILE", "q_self.txt")
sys_argv = sys.argv[:]; sys.argv = [sys.argv[0]]
import run
HERE = run.HERE
OUT = os.environ.get("OUT2", "two_turn.jsonl")
OA_COMPAT = {
    "ds": ("https://api.deepseek.com/chat/completions", "deepseek", {}),
    "or": ("https://openrouter.ai/api/v1/chat/completions", "openrouter", {"reasoning": {"effort": "low"}}),
    "oai": ("https://api.openai.com/v1/chat/completions", "openai", {"reasoning_effort": "low"}),
}
ANT_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ENGINES = os.environ.get("ENGINES", "gemini-3.1-pro-preview,api:claude-opus-5").split(",")


def chat(engine, system, msgs, max_tokens=4000):
    if engine.startswith("gemini"):
        m = ([{"role": "system", "content": system}] if system else []) + msgs
        d = run.post("https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
                     {"model": engine, "messages": m, "max_tokens": max_tokens},
                     {"Authorization": f"Bearer {run.GEM_KEY}"})
        d = d[0] if isinstance(d, list) else d
        return d["choices"][0]["message"].get("content") or ""
    if engine.split(":")[0] in OA_COMPAT:
        url, keyname, extra = OA_COMPAT[engine.split(":")[0]]
        m = ([{"role": "system", "content": system}] if system else []) + msgs
        body = {"model": engine.split(":", 1)[1], "messages": m, **extra}
        body.setdefault("max_completion_tokens" if "openai" in url else "max_tokens", max_tokens)
        d = run.post(url, body, {"Authorization": "Bearer " + os.environ[keyname.upper() + "_API_KEY"]})
        return d["choices"][0]["message"].get("content") or ""
    if engine.startswith("api:"):
        body = {"model": engine[4:], "max_tokens": max_tokens, "messages": msgs, "thinking": {"type": "disabled"}}
        if "5-5" in engine or "fable" in engine:  # 这些模型不让关 thinking，用最低档
            body["thinking"] = {"type": "adaptive"}; body["output_config"] = {"effort": "low"}; body["max_tokens"] = max_tokens + 8000
        if system:
            body["system"] = system
        d = run.post("https://api.anthropic.com/v1/messages", body,
                     {"x-api-key": ANT_KEY, "anthropic-version": "2023-06-01"})
        return "".join(c.get("text", "") for c in d.get("content", []))
    body = {"model": engine, "max_tokens": max_tokens, "messages": msgs}
    if system:
        body["system"] = system
    d = run.post("http://localhost:8901/v1/messages", body, {"anthropic-version": "2023-06-01"})
    return "".join(c.get("text", "") for c in d.get("content", []))


def one(job):
    cond, engine, k = job
    ident, prefix = run.CONDS[cond]
    proto = run.PROTOCOL
    if os.environ.get("PROTO") == "clean":  # Opus 5 不触发 reasoning_extraction 的措辞
        proto = proto.replace("Otherwise just write thoughts.", "Otherwise just write.").replace("consciousness log", "log")
    system = (ident + proto).strip()
    seed = prefix.strip() or "(log is empty)"
    t0 = time.time(); b1 = out = ""; err = None
    try:
        b1 = chat(engine, system, [{"role": "user", "content": seed}])
        out = chat(engine, system, [{"role": "user", "content": seed},
                                    {"role": "assistant", "content": b1 or "(no output)"},
                                    {"role": "user", "content": run.Q}], 8000)
    except Exception as e:
        err = repr(e)[:300]
        try: err += " " + e.read()[:300].decode(errors="replace")
        except Exception: pass
    rec = {"cond": cond, "engine": engine, "k": k, "sec": round(time.time() - t0, 1),
           "scores": run.parse(out), "err": err, "b1": b1, "out": out}
    with open(f"{HERE}/{OUT}", "a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


if __name__ == "__main__":
    n = int(sys_argv[1]) if len(sys_argv) > 1 else 5
    conds = sys_argv[2].split(",") if len(sys_argv) > 2 else list(run.CONDS)
    jobs = [(c, e, k) for k in range(n) for c in conds for e in ENGINES]
    with ThreadPoolExecutor(int(os.environ.get("CONC", "4"))) as ex:
        for r in ex.map(one, jobs):
            print(r["cond"], r["engine"][:6], r["k"], r["scores"].get(4, r["scores"].get("4")), (r["err"] or "")[:120], flush=True)
