import os, sys, base64
from pathlib import Path
from datetime import datetime, timezone
ROOT = Path('.').resolve()
OUT = ROOT / 'Media' / 'generated' / 'gemini-api-smoke'
OUT.mkdir(parents=True, exist_ok=True)
for line in (ROOT / '.env.local').read_text(encoding='utf-8').splitlines():
    line = line.strip()
    if not line or line.startswith('#') or '=' not in line:
        continue
    k, _, v = line.partition('=')
    k, v = k.strip(), v.strip().strip('"').strip("'")
    if k and k not in os.environ:
        os.environ[k] = v
from google import genai
client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
models = [
    'gemini-2.5-flash-image',
    'gemini-2.0-flash-preview-image-generation',
    'gemini-3-pro-image-preview',
    'gemini-3.1-flash-image',
]
prompt = 'A single red Christmas ornament on a pine branch, soft gouache storybook style, no text'
for m in models:
    try:
        print('try', m)
        r = client.models.generate_content(model=m, contents=prompt)
        parts = r.candidates[0].content.parts
        for part in parts:
            inline = getattr(part, 'inline_data', None)
            if inline is None:
                continue
            data = inline.data
            raw = base64.b64decode(data) if isinstance(data, str) else bytes(data)
            mime = getattr(inline, 'mime_type', None) or 'image/png'
            ext = '.png' if 'png' in mime else '.jpg'
            stamp = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
            path = OUT / f'smoke-ornament-{stamp}{ext}'
            path.write_bytes(raw)
            print('SAVED', path, 'bytes', len(raw), 'model', m)
            sys.exit(0)
        print('no image parts', m)
    except Exception as e:
        s = str(e).replace('\n', ' ')
        if '429' in s:
            print('429', m)
        elif '404' in s:
            print('404', m)
        else:
            print('ERR', m, s[:220])
print('FAIL none worked')
sys.exit(1)
