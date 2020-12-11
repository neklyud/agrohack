from fastapi import FastAPI, File, UploadFile, Form
from app.core.redis_helper import RedisHelper
import uvicorn
import asyncio
import os
import time

SHARED_PATH = "{}/../shared".format(os.path.abspath(os.environ["PYTHONPATH"]))

app = FastAPI()
redis = RedisHelper()

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

@app.post("/upload/")
async def upload_file(file: UploadFile = Form(...)):
    file.filename = "{}.jpg".format(time.strftime("%Y%m%d-%H%M%S"))
    image_destination = await save_upload_file(file)
    await publish(image_destination)
    return {
        "data": "File upload",
        "image_name": file.filename
    }

@app.get('/')
async def index():
    await publish("hello")
    return {"Hello, we!"}

if __name__ == '__main__':
    uvicorn.run(host='0.0.0.0', port=8000)
