from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class IdeaCreate(BaseModel):
    title: str
    content: str


class IdeaOut(BaseModel):
    id: int
    title: str
    content: str
    like_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }


class IdeaCommentCreate(BaseModel):
    content: str


class IdeaCommentOut(BaseModel):
    id: int
    idea_id: int
    user_id: Optional[int]
    content: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class PaginatedResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: List


class IdeaListOut(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[IdeaOut]


class IdeaCommentListOut(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[IdeaCommentOut]


