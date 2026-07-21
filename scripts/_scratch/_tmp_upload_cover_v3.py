import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv('.env.local')
os.environ['FAL_KEY'] = os.getenv('FAL_KEY') or os.getenv('FAL_API_KEY')
import fal_client
base = Path('Media/generated/cover-d-santa-peek')
for name in ['05-hearth-boots-on-feet.png','06-hearth-boots-hidden-by-sack.png','08-tree-under-gifts-no-face.png','_BASE-doorway-peek.png']:
    p = base / name
    url = fal_client.upload_file(str(p))
    print(f'{name}|{url}')
