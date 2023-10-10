import os

from fastapi import FastAPI

from model import Message
from service import MessageService
from utils.logger import get_logger

APP_PORT = 8000
SECONDARY_01_URL = os.getenv('SECONDARY_01_URL')
messages = []

logger = get_logger(__name__)

app = FastAPI()


@app.get("/")
async def read_root():
    logger.info(f'messages: {messages}')
    return {"messages": messages}


@app.post("/")
async def add_message(msg: Message):
    logger.info(f'received message: `{msg}` on server: `{__name__}`')
    msg_sent = await MessageService().send_message(msg, SECONDARY_01_URL)
    if msg_sent:
        messages.append(msg_sent)
    return msg


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)
