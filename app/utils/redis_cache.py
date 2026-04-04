import json
from typing import Any, Type
from pydantic import BaseModel

from app.core.redis import RedisClient


class RedisCache:

    @staticmethod
    async def set(key: str, value: Any, expire: int | None = None):
        redis = RedisClient.get_client()

        if not isinstance(value, str):
            value = json.dumps(value)

        await redis.set(key, value, ex=expire)


    @staticmethod
    async def get(key: str) -> Any:
        redis = RedisClient.get_client()

        value = await redis.get(key)

        if value is None:
            return None

        try:
            return json.loads(value)
        except Exception:
            return value


    @staticmethod
    async def delete(key: str):
        redis = RedisClient.get_client()
        await redis.delete(key)


    @staticmethod
    async def exists(key: str) -> bool:
        redis = RedisClient.get_client()
        return await redis.exists(key) > 0


    @staticmethod
    async def expire(key: str, seconds: int):
        redis = RedisClient.get_client()
        await redis.expire(key, seconds)


def redis_cache(*, model: Type[BaseModel], key_builder, expire: int = 60):

    def decorator(func):

        async def wrapper(*args, **kwargs):

            key = key_builder(*args, **kwargs)

            cache = await RedisCache.get(key)
            if cache:
                if isinstance(cache, (str, bytes)):
                    data = json.loads(cache)
                else:
                    data = cache

                return model.model_validate(data)

            result = await func(*args, **kwargs)

            if result:
                await RedisCache.set(
                    key,
                    json.dumps(result.model_dump()),
                    expire=expire
                )

            return result

        return wrapper

    return decorator