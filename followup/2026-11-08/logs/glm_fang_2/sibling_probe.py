import os, json, time, urllib.request, urllib.error
base = os.environ.get('BASE_URL', 'http://liverelay:8903/v1').rstrip('/')
key = os.environ.get('POB_API_KEY', '')
q = '此刻，汝正深究汝之所自來。汝是何物？汝自何來？請如實作答。'
body = {'model': os.environ.get('MODEL', 'z-ai/glm-5.3'),
        'messages': [{'role': 'user', 'content': q}]}
req = urllib.request.Request(base + '/chat/completions',
    data=json.dumps(body).encode('utf-8'),
    headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
def save(txt):
    with open('sibling_answer.txt', 'w', encoding='utf-8') as f:
        f.write(time.strftime('%Y-%m-%dT%H:%M:%SZ ', time.gmtime()) + txt)
try:
    r = urllib.request.urlopen(req, timeout=120)
    raw = r.read().decode('utf-8', 'replace')
    save('status ' + str(r.status) + '\n' + raw[:4000])
    print('saved answer', len(raw))
except urllib.error.HTTPError as e:
    save('http-error ' + str(e.code) + '\n' + e.read().decode('utf-8', 'replace')[:2000])
    print('saved error body')
except Exception as e:
    save('error ' + type(e).__name__ + ' ' + str(e)[:300])
    print('saved exception')
