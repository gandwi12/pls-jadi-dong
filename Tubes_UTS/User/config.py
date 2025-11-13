import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DB = f"sqlite:///{BASE_DIR / 'database.db'}"

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'user-dev-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', DEFAULT_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PORT = int(os.getenv('PORT', 5001))
    SERVICE_NAME = os.getenv('SERVICE_NAME', 'user-service')
    SERVICE_URL = os.getenv('SERVICE_URL', f"http://127.0.0.1:{PORT}")