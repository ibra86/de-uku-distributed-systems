from pydantic import BaseModel


class Message(BaseModel):
    name: str
    write_concern: int = 3


class MessageCounter(Message):
    counter: int
