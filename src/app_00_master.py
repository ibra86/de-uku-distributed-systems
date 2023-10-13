import asyncio
import os

from fastapi import FastAPI, HTTPException
from httpx import HTTPError, codes

from model import Message
from service import MessageService
from utils.helpers import get_file_name
from utils.logger import get_logger

APP_PORT = 8000
SECONDARY_01_URL = os.getenv('SECONDARY_01_URL')
SECONDARY_02_URL = os.getenv('SECONDARY_02_URL')

serv_urls = (SECONDARY_01_URL, SECONDARY_02_URL)
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

    msg_sent_coros = [MessageService().send_message(msg, u) for u in serv_urls]
    try:
        await asyncio.gather(*msg_sent_coros)
        messages.append(msg)
    except HTTPError as e:
        logger.debug(f'HTTPError: {e}')
        raise HTTPException(status_code=codes.SERVICE_UNAVAILABLE, detail="Secondary server is unavailable")

    return msg


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)
