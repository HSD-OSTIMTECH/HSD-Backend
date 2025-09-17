from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class FormCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = Field(default="draft")
    allow_anonymous: Optional[bool] = Field(default=False)


class FormOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    allow_anonymous: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }



