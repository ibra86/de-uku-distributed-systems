from datetime import datetime

from pydantic import BaseModel, Field


class Message(BaseModel):
    name: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
