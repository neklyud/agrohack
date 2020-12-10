from aioredis import Redis, create_redis_pool
from typing import Optional
from app.core.config.redis import RedisConfig
import asyncio

class RedisHelper:
    def __init__(self):
        self.loop = None
        self.db: str = RedisConfig.db
        self.host: str = RedisConfig.host
        self.port: str = RedisConfig.port
        self._redis: Redis
        self.url: str = "redis://localhost"

    async def connect(self) -> Redis:
        if self.loop is None:
            self.loop = asyncio.get_event_loop()
        #TODO: try/except для слета по таймайту
        self._redis = await create_redis_pool(address=self.url, loop=self.loop, timeout=10)
        return self._redis

    async def disconnect(self) -> None:
        print(self._redis)
        if self._redis:
            self._redis.close()
            await self._redis.wait_closed()

async def main():
    redis = RedisHelper()
    await redis.connect()
    await asyncio.sleep(2)
    await redis.disconnect()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
