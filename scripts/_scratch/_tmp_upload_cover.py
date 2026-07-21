import os, json
from pathlib import Path
from dotenv import load_dotenv
load_dotenv('.env.local')
key = os.getenv('FAL_KEY') or os.getenv('FAL_API_KEY')
assert key, 'no FAL key'
os.environ['FAL_KEY'] = key
import fal_client
path = Path('Media/generated/cover-d-santa-peek/_BASE-doorway-peek.png')
if not path.exists():
    path = Path('Media/approved/style-refs/covers/D-front-doorway-peek.png')
url = fal_client.upload_file(str(path))
print(url)
