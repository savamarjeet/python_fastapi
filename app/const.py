import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DB_FILE_PATH = os.path.join(BASE_DIR, os.getenv('DATABASE_NAME'))

ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 60 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")   # should be kept secret
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")
DATABASE_URI = f"sqlite:///{DB_FILE_PATH}"
