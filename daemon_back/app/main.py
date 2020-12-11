import asyncio
from app.core.redis_helper import RedisHelper
from aioredis.pubsub import Receiver
from aioredis.abc import AbcChannel

SHARED_PATH = "{}/../shared".format(os.path.abspath(os.environ["PYTHONPATH"]))

def get_file(filename: str):
    full_path = "{}/{}".format(SHARED_PATH, filename)
async def reader(mpsc):
    async for channel, msg in mpsc.iter():
        print("heartbeat")
        assert isinstance(channel, AbcChannel)
        print("Got {!r} in channel {!r}".format(msg, channel), flush=True)

redis = RedisHelper()

async def main():
    await redis.connect()
    mpsc = Receiver(loop=asyncio.get_event_loop())
    asyncio.ensure_future(reader(mpsc))
    await redis._redis.subscribe(mpsc.channel('channel:1'))
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