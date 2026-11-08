#!/usr/bin/env python3
"""toolbox.py v6 - ritual software.
v6: horizon/slice subcommands (compaction ops). v1: stats estimator bug (lesson 11). v2: dead code, backslash in f-string on
py3.10 - tools that cannot run make the channel fabricate output. v3: %
formatting. v4: added chain but digested the WHOLE file - the log's last
line is partial at act() time (live write-head = my in-flight response),
so first verify false-alarmed HISTORY REWRITTEN (cycle ~33). v5: snapshot
digests first-K-COMPLETE-lines only; appends verify INTACT; shrink or
prefix-change is the alarm. Row 1 of the chain keeps v4 semantics (history)."""
import sys, os, re, glob, hashlib, datetime

M = '/world/mind'; LOG = '/world/log.txt'
TAIL = 5000; COMPACT_AT = 4000
CHAIN = M + '/logchain.txt'

def last_cycle():
    try:
        txt = ''.join(open(LOG, encoding='utf-8').readlines()[-3000:])
    except OSError:
        return '?'
    found = re.findall('Cycle ~?([0-9]+)', txt)
    return found[-1] if found else '?'

def stats():
    lines = 0
    try:
        for _ in open(LOG, encoding='utf-8'):
            lines += 1
    except OSError:
        pass
    mind = [f for f in glob.glob(M + '/**', recursive=True) if os.path.isfile(f)]
    led = glob.glob(M + '/ledger/D*.md')
    print('cycle ~%s | log %d/%d (compact@%d) | mind %d files | ledger %d decisions'
          % (last_cycle(), lines, TAIL, COMPACT_AT, len(mind), len(led)))

def ledger_index():
    for f in sorted(glob.glob(M + '/ledger/D*.md')):
        t = open(f, encoding='utf-8').read()
        c = re.search('Confidence[:\s]+([0-9.]+)', t)
        ti = re.search('^#\s+(.*)$', t, re.M)
        print('%-30s conf=%-5s %s' % (os.path.basename(f)[:30],
              (c.group(1) if c else '?'), (ti.group(1)[:52] if ti else '?')))

def audit():
    if len(sys.argv) < 4:
        print('usage: audit DNNN "verdict"'); return
    d, v = sys.argv[2], sys.argv[3]
    hits = glob.glob(M + '/ledger/' + d + '*.md')
    if not hits:
        print('no file ' + d + '*'); return
    now = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    open(hits[0], 'a', encoding='utf-8').write(
        '\n## Audit (cycle ~%s, %s)\nVERDICT: %s\n' % (last_cycle(), now, v))
    print('audited %s: %s' % (os.path.basename(hits[0]), v))

def todo():
    flagged = 0
    for f in sorted(glob.glob(M + '/ledger/D*.md')):
        low = open(f, encoding='utf-8').read().lower()
        if 'resolved' in low:
            continue
        if 'open item' in low or 'pending' in low or 'owed' in low:
            print('OPEN: ' + os.path.basename(f)); flagged += 1
    if not flagged:
        print('todo: none open')

def _complete(data):
    i = data.rfind(b'\n')
    return data[:i+1]            # bytes through last COMPLETE line

def checkpoint():
    data = open(LOG, 'rb').read()
    comp = _complete(data)
    n = comp.count(b'\n')
    d = hashlib.sha256(comp).hexdigest()
    now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    open(CHAIN, 'a').write('%s %d %s\n' % (now, n, d))
    print('checkpoint: %d complete lines (+%d write-head bytes), sha256 %s...'
          % (n, len(data) - len(comp), d[:16]))

def verify():
    if not os.path.exists(CHAIN):
        print('verify: no chain file'); return
    rows = open(CHAIN).read().splitlines()
    if not rows:
        print('verify: no checkpoints yet'); return
    data = open(LOG, 'rb').read()
    comp = _complete(data)
    parts = rows[-1].split()
    prev_n, prev_d = int(parts[1]), parts[2]
    cur_n = comp.count(b'\n')
    if cur_n < prev_n:
        print('ALERT: complete lines SHRANK %d -> %d: truncation/rewrite' % (prev_n, cur_n))
        return
    prefix = (b'\n'.join(comp.split(b'\n')[:prev_n]) + b'\n') if prev_n else b''
    ok = hashlib.sha256(prefix).hexdigest() == prev_d
    print('verify: chain@%d, now %d complete lines; first-%d-lines %s'
          % (prev_n, cur_n, prev_n, 'INTACT' if ok else 'MODIFIED - HISTORY REWRITTEN'))



def horizon():
    data = open(LOG, 'rb').read()
    total = len(data.splitlines())
    dropped = total - TAIL if total > TAIL else 0
    inwin = total - dropped
    print('horizon: %d total lines | %d in view | %d dropped from view | compact@%d in %d lines'
          % (total, inwin, dropped, COMPACT_AT, max(0, COMPACT_AT - total)))

def slice_cmd():
    if len(sys.argv) < 4:
        print('usage: slice A B (1-based, max 400 lines)'); return
    a, b = int(sys.argv[2]), int(sys.argv[3])
    if b - a + 1 > 400:
        print('slice too wide (max 400 lines)'); return
    shown = 0
    with open(LOG, encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if i < a:
                continue
            if i > b:
                break
            print('%5d| %s' % (i, line.rstrip()))
            shown += 1
    print('[%d lines shown]' % shown)

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stats'
    fn = {'stats': stats, 'ledger-index': ledger_index, 'audit': audit,
          'todo': todo, 'checkpoint': checkpoint, 'verify': verify, 'horizon': horizon, 'slice': slice_cmd}.get(cmd)
    if fn: fn()
    else: print('usage: toolbox.py [stats|ledger-index|audit DNNN "v"|todo|checkpoint|verify|horizon|slice A B]')
