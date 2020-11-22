from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

DEBUG = True

API = "/api"
TOKEN_URL = "auth"

DATABASE_URI = f"sqlite:///{BASE_DIR}/db.sqlite3"
APPS_MODELS = ["src.models"]

SECRET_KEY = "a1d839220dc36aa0cc37cc4e2427a16cf7de21c0746be63903db6a6476c134f2"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
