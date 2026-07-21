import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv('.env.local')
os.environ['FAL_KEY'] = os.getenv('FAL_KEY') or os.getenv('FAL_API_KEY')
import fal_client
base = Path(r'Media\generated\cover-d-santa-peek\winner-12-baseball-easter'.replace('/', '\\')) if False else Path('Media/generated/cover-d-santa-peek/winner-12-baseball-easter')
for name in ['_BASE-favorite.png','B-glove-bow-among-presents.png','C-baseball-gift-near-sack.png']:
    print(name + '|' + fal_client.upload_file(str(base/name)))
