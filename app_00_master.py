import logging
import os
from datetime import datetime

import backoff
from fastapi import FastAPI, HTTPException
from httpx import AsyncClient, codes, ConnectError, HTTPError
from pydantic import BaseModel, Field

SERVICE_NAME = 'master'

logging.basicConfig()
logger = logging.getLogger(SERVICE_NAME)
logger.setLevel(logging.DEBUG)

APP_PORT = 8000

SECONDARY_01_URL = os.getenv('SECONDARY_01_URL')

app = FastAPI()

messages = []


class Message(BaseModel):
    name: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


@app.get("/")
async def read_root():
    logger.info(f'messages: {messages}')
    return {"messages": messages}


@app.post("/")
async def add_message(msg: Message):
    logger.info(f'received message: `{msg}` on server: `{SERVICE_NAME}`')
    try:
        # status_code = await send_msg(msg, 'localhost:8001')
        status_code = await send_msg(msg, SECONDARY_01_URL)

        if status_code == codes.OK:
            messages.append(msg)
            logger.info(f'message is replicated on secondary servers')
            return msg
        else:
            raise

    except HTTPError as e:
        logger.debug(f'HTTPError: {e}')
        raise HTTPException(status_code=codes.SERVICE_UNAVAILABLE, detail="Secondary server is unavailable")


@backoff.on_exception(backoff.expo, ConnectError, max_time=3)
async def send_msg(msg, url):
    try:
        async with AsyncClient() as client:
            resp = await client.post(url=url,
                                     json=dict(msg),
                                     headers={"Content-Type": "application/json"}
                                     )
            resp.raise_for_status()
        return resp.status_code
    except HTTPError:
        raise


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)
