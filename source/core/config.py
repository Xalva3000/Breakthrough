from pathlib import Path
import logging



BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_URL_STORAGE_PATH = BASE_DIR / "short_url_storage.json"
LOG_LEVEL = logging.INFO

# print(BASE_DIR)

API_TOKENS: frozenset[str] = frozenset(
    {
        'Q7ur4lcBhh3kS6_mY0ZxBQ',
        'wzmBDdEE9fI71Fka4JeeDw',
        'qwerty'
    }
)

USERS_DB: dict[str, str] = {
    "Xalva": "qwerty",
    "WillieDvin": "qwerty"
}