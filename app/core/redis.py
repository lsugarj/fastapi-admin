from redis.asyncio import Redis
from typing import Optional

from app.core.config import get_settings


class RedisClient:
    _client: Optional[Redis] = None

    @classmethod
    async def init(cls):
        redis_config = get_settings().redis
        url = f"redis://{redis_config.host}:{redis_config.port}/{redis_config.db}"
        if cls._client is not None:
            return
        cls._client = Redis.from_url(
            url,
            encoding="utf-8",
            decode_responses=True
        )

    @classmethod
    def get_client(cls) -> Redis:
        if cls._client is None:
            raise RuntimeError("Redis 未初始化")
        return cls._client

    @classmethod
    async def close(cls):
        if cls._client:
            await cls._client.close()
            cls._client = None