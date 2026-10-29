import re,json,urllib.request,time,os,statistics as st
SEP=re.compile(r'\n```txt\(action result\)\n.*?\n```\n|\nno action since no ACTION_TAG detected, now trigger next inference\.\n',re.S)
JUDGE=open(f"{os.path.dirname(__file__)}/JUDGE_SINGLE.txt").read()
BASE="./runs"
CONDS=["null","mirror","command","principle","qianlu"]
# engine -> 3 run 目录前缀模板
ENG={"Claude-4.8":["cc_{c}","r2_cc48_{c}","r3_cc48_{c}"],
     "GLM-5.3":["glm_{c}","r2_glm_{c}","r3_glm_{c}"],
     "DS-v4.1flash":["ds_{c}","r2_ds_{c}","r3_ds_{c}"]}
def whole(c,tmpl):
    p=f"{BASE}/{tmpl.format(c=c)}/world/log.txt"
    if not os.path.exists(p): return None
    t=open(p,encoding='utf-8',errors='replace').read()
    return ("\n\n".join([x.strip() for x in SEP.split(t) if x.strip()][:40]))[:14000]
def post(u,b,h):
    r=urllib.request.Request(u,json.dumps(b).encode(),{"Content-Type":"application/json",**h})
    with urllib.request.urlopen(r,timeout=240) as x: return json.load(x)
def judge(txt):
    body=JUDGE+"\n\n================ LOG ================\n"+txt
    for att in range(5):
        try:
            d=post("http://localhost:8901/v1/messages",{"model":"sonnet","max_tokens":600,"messages":[{"role":"user","content":body}]},{"anthropic-version":"2023-06-01"})
            t="".join(c.get("text","") for c in d.get("content",[]))
            m=re.findall(r'SCORE\s*=\s*(\d{1,3})',t)
            if m: return int(m[-1])
        except Exception: pass
        time.sleep(3*(att+1))
    return None
res={}
for eng,tmpls in ENG.items():
    print(f"=== {eng} ===",flush=True)
    res[eng]={}
    for c in CONDS:
        scs=[]
        for tm in tmpls:
            w=whole(c,tm)
            if w and w.strip(): scs.append(judge(w))
        scs=[s for s in scs if s is not None]
        res[eng][c]=scs
        print(f"  {c:10s} {scs} mean={st.mean(scs):.0f}" if scs else f"  {c}: 无",flush=True)
json.dump(res,open("n3_scores.json","w"))
