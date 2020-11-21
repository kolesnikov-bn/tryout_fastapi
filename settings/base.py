from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

DEBUG = True

API = "/api"

DATABASE_URI = f"sqlite:///{BASE_DIR}/db.sqlite3"
APPS_MODELS = ["src.product.models", "src.user.models"]
