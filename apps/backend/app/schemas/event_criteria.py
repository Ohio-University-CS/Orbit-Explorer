from pydantic import BaseModel, Field

class EventCriteria(BaseModel):
    """Describes criteria for astronomical events."""
    name: str
    description: str