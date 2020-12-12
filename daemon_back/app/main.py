import asyncio
from app.core.redis_helper import RedisHelper
from app.core.model import Model
from aioredis.pubsub import Receiver
from aioredis.abc import AbcChannel
import os

SHARED_PATH = "{}/../shared".format(os.path.abspath(os.environ["PYTHONPATH"]))


#model = Model()


def get_full_path(filename: str):
    full_path = "{}/{}".format(SHARED_PATH, filename)
    return full_path


async def reader(mpsc):
    async for channel, msg in mpsc.iter():
        assert isinstance(channel, AbcChannel)
        full_path = get_full_path(msg)
        #model.predict(full_path)
        print(full_path)
        print("Got {!r} in channel {!r}".format(msg, channel), flush=True)

redis = RedisHelper()

async def main():
    await redis.connect()
    asyncio.ensure_future(reader(redis.receiver))
    await redis.subscribe()
    while True:
        try:
            await asyncio.sleep(10)
            print('hearbeat', flush=True)
        except Exception as ex:
            print(ex, flush=True)
            mpsc.stop()
            await redis.disconnect()

if __name__ == '__main__':
    asyncio.run(main())