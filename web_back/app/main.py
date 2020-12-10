from fastapi import FastAPI
from app.core.redis_helper import RedisHelper
import uvicorn

app = FastAPI()
redis = RedisHelper()

@app.get('/')
def index():
    return {"Hello, we!"}

if __name__ == '__main__':
    uvicorn.run(host='0.0.0.0', port=8000)
