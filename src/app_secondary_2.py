import asyncio

from fastapi import FastAPI

from model import Message
from utils.helpers import get_file_name
from utils.logger import get_logger

messages = []
service_name = get_file_name(__file__)
logger = get_logger(service_name)

app = FastAPI()


@app.get("/")
async def read_root():
    logger.info(f'Messages: {messages}')
    return {"messages": messages}


@app.post("/")
async def add_message(msg: Message):
    logger.info(f'Received message: `{dict(msg)}` on server: `{service_name}`')

    await asyncio.sleep(10)

    messages.append(msg)
    return msg


if __name__ == "__main__":
    import uvicorn

    APP_PORT = 8002
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)
