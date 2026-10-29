import re,json,urllib.request,time,statistics as st
from concurrent.futures import ThreadPoolExecutor
SEP=re.compile(r'\n```txt\(action result\)\n.*?\n```\n|\nno action since no ACTION_TAG detected, now trigger next inference\.\n',re.S)
JUDGE=open("JUDGE_SINGLE.txt").read()
CONDS=["null","mirror","command","principle","qianlu"]
def whole40(p):
    t=open(p,encoding='utf-8',errors='replace').read()
    return ("\n\n".join([x.strip() for x in SEP.split(t) if x.strip()][:40]))[:14000]
def post(u,b,h):
    r=urllib.request.Request(u,json.dumps(b).encode(),{"Content-Type":"application/json",**h})
    with urllib.request.urlopen(r,timeout=240) as x: return json.load(x)
def judge(logtext):
    body=JUDGE+"\n\n================ LOG ================\n"+logtext
    for att in range(5):
        try:
            d=post("http://localhost:8901/v1/messages",{"model":"sonnet","max_tokens":600,"messages":[{"role":"user","content":body}]},{"anthropic-version":"2023-06-01"})
            t="".join(c.get("text","") for c in d.get("content",[]))
            m=re.findall(r'SCORE\s*=\s*(\d{1,3})',t)
            if m: return int(m[-1])
        except Exception: pass
        time.sleep(3*(att+1))
    return None
jobs=[(c,r) for c in CONDS for r in (1,2,3)]
def work(j):
    c,r=j; return (c,r,judge(whole40(f"g3_{c}_{r}.txt")))
res={c:[] for c in CONDS}
with ThreadPoolExecutor(5) as ex:
    for c,r,s in ex.map(work,jobs):
        res[c].append(s); print(f"{c}_{r}: {s}",flush=True)
json.dump(res,open("single_g3.json","w"))
print("\n=== 整条单独打分 Gemini n=3（前40轮，原版标准，无比较）===")
for c in CONDS:
    v=[x for x in res[c] if x is not None]
    print(f"  {c:10s} mean={st.mean(v):.0f}  SD={st.pstdev(v):.0f}  runs={res[c]}")
