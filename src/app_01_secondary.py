import logging

from fastapi import FastAPI

from model import Message

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

APP_PORT = 8001

app = FastAPI()

messages = []


@app.get("/")
async def read_root():
    logger.info(f'messages: {messages}')
    return {"messages": messages}


@app.post("/")
async def add_message(msg: Message):
    logger.info(f'received message: `{msg}` on server: `{__name__}`')
    messages.append(msg)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)
