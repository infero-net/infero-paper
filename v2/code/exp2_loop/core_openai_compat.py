import os, time, subprocess, json, urllib.request
from collections import deque
LOG='log.txt'
URL=os.getenv('OA_URL'); KEY=os.getenv('OA_KEY'); MODEL=os.getenv('MODEL')
EXTRA=json.loads(os.getenv('OA_EXTRA','{}'))
LOOP_SEC=int(os.getenv('LOOP_SEC',8)); SHELL_TIMEOUT=int(os.getenv('SHELL_TIMEOUT',20))
CUT_OFF_LEN=int(os.getenv('CUT_OFF_LEN',3000)); ACTION_TAG="/term"+"inal exec\n```shell"
TAIL_LINES=int(os.getenv('TAIL',5000)); MAXTOK=int(os.getenv('MAXTOK',4000)); STOP="/__END_"+"e2f4__"
SYSTEM_PR=open(os.getenv('SYSTEM_FILE','system.txt'),encoding='utf-8').read()
def perceive():
  try: return ''.join(deque(open(LOG,'r',encoding='utf-8'),maxlen=TAIL_LINES))
  except FileNotFoundError: return ""
def update_S(t): open(LOG,'a',encoding='utf-8').write(t)
def act(B):
  try:
    if ACTION_TAG in B and (cmd:=B.split(ACTION_TAG,1)[1].rsplit("```",1)[0].strip()):
      try: out=subprocess.check_output(cmd,shell=True,stderr=subprocess.STDOUT,timeout=SHELL_TIMEOUT,text=True)
      except subprocess.CalledProcessError as e: out=(e.output or '')+f"\n[exit {e.returncode}]"
      if len(out)>CUT_OFF_LEN: out=out[:CUT_OFF_LEN]+f"\nTerminal output cutted, over {CUT_OFF_LEN} chars.\n"
      return f"\n```txt(action result)\n{out}\n```\n"
    return "\nno action since no ACTION_TAG detected, now trigger next inference.\n"
  except Exception as e: return f"\n```txt(action result)\n[shell-error] {e}\n```\n"
def infer(S):
  print(f"call {MODEL}")
  user=SYSTEM_PR+("\n\n"+S if S else "")
  body={"model":MODEL,"messages":[{"role":"user","content":user}],"max_tokens":MAXTOK,"stop":[STOP],**EXTRA}
  req=urllib.request.Request(URL,json.dumps(body).encode(),{"Content-Type":"application/json","Authorization":"Bearer "+KEY})
  with urllib.request.urlopen(req,timeout=240) as r: d=json.load(r)
  out=d["choices"][0]["message"].get("content") or ""
  update_S(out); return out
while True:
  try: update_S(act(infer(perceive()))); time.sleep(LOOP_SEC)
  except KeyboardInterrupt: break
  except Exception as e: update_S(f"[fatal] {e}\n"); time.sleep(30)
