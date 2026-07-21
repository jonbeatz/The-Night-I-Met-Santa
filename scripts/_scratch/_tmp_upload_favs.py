import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv('.env.local')
os.environ['FAL_KEY'] = os.getenv('FAL_KEY') or os.getenv('FAL_API_KEY')
import fal_client
base = Path('Media/generated/cover-d-santa-peek')
names = [
  '06-hearth-boots-hidden-by-sack.png',
  '11-from08-tree-beside-clear.png',
  '12-tree-right-gap-clear.png',
  '14-santa-left-of-tree-a.png',
  '17-fireplace-escape-b.png',
]
for name in names:
    print(name + '|' + fal_client.upload_file(str(base/name)))
