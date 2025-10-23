from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TimestampedModel(BaseModel):
    """Base model with automatic timestamp metadata."""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True
