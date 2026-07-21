import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv('.env.local')
k = os.getenv('FAL_KEY') or os.getenv('FAL_API_KEY')
print('key_len', len(k) if k else 0)
os.environ['FAL_KEY'] = k
import fal_client
p = Path('Media/generated/cover-d-santa-peek/winner-12-baseball-easter/D-combo-glove-front-bat-fireplace-c.png')
print(fal_client.upload_file(str(p)))
