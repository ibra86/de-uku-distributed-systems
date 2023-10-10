import os

from fastapi import FastAPI

from model import Message
from service import MessageService
from utils.helpers import get_file_name
from utils.logger import get_logger

APP_PORT = 8000
SECONDARY_01_URL = os.getenv('SECONDARY_01_URL')
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
    msg_sent = await MessageService().send_message(msg, SECONDARY_01_URL)
    if msg_sent:
        messages.append(msg_sent)
    return msg


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)
