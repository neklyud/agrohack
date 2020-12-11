from fastapi import FastAPI, File, UploadFile, Form
from app.core.redis_helper import RedisHelper
import uvicorn
import asyncio

async def main(redis):
    await redis.connect()
    await asyncio.sleep(2)
    await redis.disconnect()


app = FastAPI()
redis = RedisHelper()

async def publish(message: str):
    await redis.connect()
    await redis.publish_message(message)
    await redis.disconnect()
    print(redis._redis.channels, flush=True)

@app.post("/upload/")
async def upload_file(file: str = Form(...)):
    return {
        "length": len(file)
    }

@app.get('/')
async def index():
    await publish("hello")
    return {"Hello, we!"}

if __name__ == '__main__':
    uvicorn.run(host='0.0.0.0', port=8000)
