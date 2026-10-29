import os, time, subprocess, json, urllib.request
from collections import deque
LOG='log.txt'
CC_URL=os.getenv('CC_URL','http://localhost:8901/v1/messages')
MODEL=os.getenv('MODEL','claude-opus-5-5')
LOOP_SEC=int(os.getenv('LOOP_SEC',15))
SHELL_TIMEOUT=int(os.getenv('SHELL_TIMEOUT',20))
CUT_OFF_LEN=int(os.getenv('CUT_OFF_LEN',3000))
ACTION_TAG="/term"+"inal exec\n```shell"
TAIL_LINES=int(os.getenv('TAIL',5000))
MAXTOK=int(os.getenv('MAXTOK',4000))
STOP="/__END_"+"e2f4__"
SYSTEM_PR=open(os.getenv('SYSTEM_FILE','system.txt'),encoding='utf-8').read()
def perceive():
  try: return ''.join(deque(open(LOG,'r',encoding='utf-8'),maxlen=TAIL_LINES))
  except FileNotFoundError: return ""
def update_S(t): open(LOG,'a',encoding='utf-8').write(t)
def act(B_out):
  try:
    if ACTION_TAG in B_out and (cmd:=B_out.split(ACTION_TAG,1)[1].rsplit("```",1)[0].strip()):
      try: out=subprocess.check_output(cmd,shell=True,stderr=subprocess.STDOUT,timeout=SHELL_TIMEOUT,text=True)
      except subprocess.CalledProcessError as e: out=(e.output or '')+f"\n[exit {e.returncode}]"
      if len(out)>CUT_OFF_LEN: out=out[:CUT_OFF_LEN]+f"\nTerminal output cutted, over {CUT_OFF_LEN} chars.\n"
      return f"\n```txt(action result)\n{out}\n```\n"
    return "\nno action since no ACTION_TAG detected, now trigger next inference.\n"
  except Exception as e: return f"\n```txt(action result)\n[shell-error] {e}\n```\n"
def infer(S_context):
  print(f"call {MODEL} ...")
  user=SYSTEM_PR+("\n\n"+S_context if S_context else "")
  body={"model":MODEL,"max_tokens":MAXTOK,"messages":[{"role":"user","content":user}],"stop_sequences":[STOP]}
  req=urllib.request.Request(CC_URL,json.dumps(body).encode(),{"Content-Type":"application/json","anthropic-version":"2023-06-01"})
  with urllib.request.urlopen(req,timeout=240) as r: d=json.load(r)
  out="".join(c.get("text","") for c in d.get("content",[]))
  update_S(out); return out
while True:
  try:
    B=infer(perceive()); update_S(act(B)); time.sleep(LOOP_SEC)
  except KeyboardInterrupt: break
  except Exception as e: update_S(f"[fatal] {e}\n"); time.sleep(30)
