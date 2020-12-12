from fastapi import FastAPI, File, UploadFile, Form, WebSocket
from app.core.redis_helper import RedisHelper
import uvicorn
import asyncio
import os
import time
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from aioredis.pubsub import Receiver

SHARED_PATH = "{}/../shared".format(os.path.abspath(os.environ["PYTHONPATH"]))


app = FastAPI()
redis = RedisHelper()

ALLOWED_HOSTS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def save_upload_file(upload_file: UploadFile):
    destination = "{}/{}".format(SHARED_PATH, upload_file.filename)
    print(destination)
    try:
        with open(destination, "wb+") as file_object:
            file_data = await upload_file.read()
            file_object.write(file_data)
    except Exception as ex:
        print(ex)
    return upload_file.filename
        

async def publish(message: str):
    await redis.connect()
    await redis.publish_message(message)
    await redis.disconnect()
    print(redis._redis.channels, flush=True)

async def reader(mpsc):
    async for channel, msg in mpsc.iter():
        assert isinstance(channel, AbcChannel)
        return msg

async def listen_input_channel():
    await redis.connect()
    mspc = Receiver(loop=asyncio.get_event_loop())
    msg = await reader(mspc)
    await redis.subscribe(mpsc.channel('channel:2'))
    await redis.disconnect()
    return msg


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file.filename = "{}.jpg".format(time.strftime("%Y%m%d-%H%M%S"))
        image_destination = await save_upload_file(file)
        await publish(image_destination)
    except Exception as ex:
        return jsonable_encoder({
                "image_name": file.filename,
                "error": "err",
        })
    return jsonable_encoder({
            "image_name": file.filename,
            "error": None,
        })

@app.websocket("/ws")
async def get_result_endpoint(websocket: WebSocket):
    await websocket.accept()
    data = await listen_input_channel()
    await websocket.send_text(data)
    await websocket.close()

@app.get('/')
async def index():
    await publish("hello")
    return {"Hello, we!"}

if __name__ == '__main__':
    uvicorn.run(host='0.0.0.0', port=8000)
