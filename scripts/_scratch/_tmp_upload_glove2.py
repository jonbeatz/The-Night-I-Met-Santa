import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv('.env.local')
os.environ['FAL_KEY'] = os.getenv('FAL_KEY') or os.getenv('FAL_API_KEY')
import fal_client
base = Path('Media/generated/cover-d-santa-peek/winner-12-baseball-easter')
for name in ['D-combo-glove-front-bat-fireplace-c.png','ref-replace-stuffed.png','ref-move-glove.png']:
    print(name + '|' + fal_client.upload_file(str(base/name)))
