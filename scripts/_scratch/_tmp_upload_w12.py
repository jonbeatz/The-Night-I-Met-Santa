import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv('.env.local')
os.environ['FAL_KEY'] = os.getenv('FAL_KEY') or os.getenv('FAL_API_KEY')
import fal_client
p = Path('Media/generated/cover-d-santa-peek/WINNER-12-base.png')
print(fal_client.upload_file(str(p)))
