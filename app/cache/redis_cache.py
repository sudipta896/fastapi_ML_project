import json
import os
import redis
from dotenv import load_dotenv
from app.core.config import settings


# load_dotenv()

# REDIS_URL = os.getenv("REDIS_URL")

redis_client = redis.Redis.from_url(settings.REDIS_URL)


def get_cached_prediction(key: str):
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    return None


def set_cached_prediction(key: str, value: dict, expire_seconds: int = 3600):
    redis_client.setex(key, expire_seconds, value=json.dumps(value))
