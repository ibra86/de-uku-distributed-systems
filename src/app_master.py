import asyncio

from fastapi import FastAPI, HTTPException
from httpx import codes

from init_secondaries import SECONDARY_SERVERS_URLS
from model import Message
from service import MessageService
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

    msg_sent_coros = [MessageService().send_message(msg, u) for u in SECONDARY_SERVERS_URLS]

    resp = await asyncio.gather(*msg_sent_coros, return_exceptions=True)

    rcv_write_concern = len([r for r in resp if isinstance(r, Message)]) + 1
    if rcv_write_concern >= msg.write_concern:
        messages.append(msg)
        return msg
    else:
        raise HTTPException(status_code=codes.GATEWAY_TIMEOUT,
                            detail=f"Received Write concern: {rcv_write_concern}, but should be {msg.write_concern}")


if __name__ == "__main__":
    import uvicorn

    APP_PORT = 8000
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)
