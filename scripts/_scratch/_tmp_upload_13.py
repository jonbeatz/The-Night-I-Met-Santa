import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv('.env.local')
os.environ['FAL_KEY'] = os.getenv('FAL_KEY') or os.getenv('FAL_API_KEY')
import fal_client
base = Path('Media/generated/cover-d-santa-peek')
for name in ['13-hearth-05-06-blend.png','_BASE-doorway-peek.png']:
    print(name + '|' + fal_client.upload_file(str(base/name)))
