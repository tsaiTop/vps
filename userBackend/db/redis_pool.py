import aioredis
import os
# from core.config import config

def create_redis_connect():
    try:
        redis = aioredis.from_url(
            os.getenv("REDIS_URL"),
            encoding="utf-8",
            decode_responses=True,
        )
        return redis
    except Exception as e:
        print(e)
  