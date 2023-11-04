from fastapi import FastAPI

from model import MessageCounter
from utils.helpers import get_file_name, sleep_ms, cleanup
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
async def add_message(msg_cnt: MessageCounter):
    logger.info(f'Received message: `{dict(msg_cnt)}` on server: `{service_name}`')

    s = await sleep_ms()
    logger.info(f'Slept: `{s}` ms on server: `{service_name}`')

    global messages
    messages.append(msg_cnt)
    messages = cleanup(messages)  # reorder and deduplication
    return msg_cnt


if __name__ == "__main__":
    import uvicorn

    APP_PORT = 8001
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)
