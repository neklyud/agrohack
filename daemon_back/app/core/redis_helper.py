from aioredis import Redis, create_redis_pool
from typing import Optional
from aioredis.pubsub import Receiver
from app.core.config.redis import RedisConfig
import asyncio

class RedisHelper:
    def __init__(self, url = "redis://redis:6379"):
        self.loop = None
        self.db: str = RedisConfig.db
        self.host: str = RedisConfig.host
        self.port: str = RedisConfig.port
        self._redis: Redis
        self.url: str = url

    async def connect(self) -> Redis:
        if self.loop is None:
            self.loop = asyncio.get_event_loop()
        #TODO: try/except для слета по таймайту
        self._redis = await create_redis_pool(address=self.url, loop=self.loop, timeout=10)
        pong = await self._redis.ping()
        print(pong)
        return self._redis

    async def disconnect(self) -> None:
        print(self._redis)
        if self._redis:
            self._redis.close()
            await self._redis.wait_closed()

