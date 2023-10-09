import logging

from fastapi import FastAPI
from pydantic import BaseModel

SERVICE_NAME = 'secondary_01'

logging.basicConfig()
logger = logging.getLogger(SERVICE_NAME)
logger.setLevel(logging.DEBUG)

APP_PORT = 8001

app = FastAPI()

messages = []


class Message(BaseModel):
    name: str
    timestamp: str = None


@app.get("/")
async def read_root():
    logger.info(f'messages: {messages}')
    return {"messages": messages}


@app.post("/")
async def add_message(msg: Message):
    logger.info(f'received message: `{msg}` on server: `{SERVICE_NAME}`')
    messages.append(msg)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)
