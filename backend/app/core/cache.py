# app/core/cache.py
import aioredis
from contextlib import asynccontextmanager
from app.core.config import settings
from typing import Optional, Any

class RedisCache:
    _instance = None

    def __init__(self):
        self.redis = None

    @classmethod
    @asynccontextmanager
    async def get_instance(cls):
        if cls._instance is None:
            cls._instance = RedisCache()
            await cls._instance.connect()
        yield cls._instance
        await cls._instance.disconnect()

    async def connect(self):
        self.redis = await aioredis.create_redis_pool(settings.REDIS_URL)

    async def disconnect(self):
        if self.redis:
            self.redis.close()
            await self.redis.wait_closed()

    async def set(self, key: str, value: Any, expire: int = 3600) -> None:
        """Сохранить значение в кэше с временем истечения (по умолчанию 1 час)."""
        await self.redis.set(key, str(value), expire=expire)

    async def get(self, key: str) -> Optional[str]:
        """Получить значение из кэша."""
        value = await self.redis.get(key)
        return value.decode() if value else None

    async def delete(self, key: str) -> None:
        """Удалить ключ из кэша."""
        await self.redis.delete(key)

# Пример использования (для сервисов)
async def get_cache():
    async with RedisCache.get_instance() as cache:
        yield cache