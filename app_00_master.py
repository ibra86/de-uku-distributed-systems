from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

messages = []


class Message(BaseModel):
    name: str
    description: str = None


@app.get("/")
async def read_root():
    return {"messages": messages}


@app.post("/")
async def add_message(msg: Message):
    messages.append(msg)
    return msg


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
