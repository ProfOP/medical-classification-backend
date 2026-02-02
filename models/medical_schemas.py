from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime


class MedicalArtifactCreate(BaseModel):
    type: str
    title: str
    data: Any
    source: Optional[str] = "manual"
    event_date: Optional[datetime] = None


class MedicalArtifactResponse(BaseModel):
    id: int
    type: str
    title: str
    data: Any
    source: str
    event_date: Optional[datetime]
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
