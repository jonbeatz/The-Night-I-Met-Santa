import os, json, urllib.request
from pathlib import Path
from dotenv import load_dotenv
load_dotenv('.env.local')
key = os.getenv('FAL_API_KEY') or os.getenv('FAL_KEY')
path = Path('Media/generated/cover-d-santa-peek/winner-12-baseball-easter/D-combo-glove-front-bat-fireplace-c.png')
req = urllib.request.Request(
    'https://rest.alpha.fal.ai/storage/upload/initiate',
    data=json.dumps({'file_name': path.name, 'content_type': 'image/png'}).encode(),
    headers={'Authorization': f'Key {key}', 'Content-Type': 'application/json'},
    method='POST',
)
try:
    with urllib.request.urlopen(req) as r:
        meta = json.loads(r.read().decode())
    print('initiate', meta)
    upload_url = meta['upload_url']
    file_url = meta['file_url']
    data = path.read_bytes()
    put = urllib.request.Request(upload_url, data=data, method='PUT', headers={'Content-Type': 'image/png'})
    with urllib.request.urlopen(put) as r:
        print('put_status', r.status)
    print('FILE_URL', file_url)
except Exception as e:
    print('ERR', type(e), e)
    if hasattr(e, 'read'):
        print(e.read().decode())
