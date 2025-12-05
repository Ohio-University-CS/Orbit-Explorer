from pydantic import BaseModel, Field
from datetime import datetime

class EventItem(BaseModel):
    id: str
    type: str
    name: str
    time: datetime
    desc: str
