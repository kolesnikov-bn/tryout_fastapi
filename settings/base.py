from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

DATABASE_URI = f"sqlite:///{BASE_DIR}/db.sqlite3"
API = "/api"


APPS_MODELS = []
