from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import UniqueConstraint

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    start_date: Optional[str] = None  # Tarih formatı: 'YYYY-MM-DD'
    end_date: Optional[str] = None
    image_url: Optional[str] = None


class Form(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    status: str = Field(default="draft")  # e.g., draft|published|archived
    allow_anonymous: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)


class Idea(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)


class IdeaLike(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("idea_id", "user_id", name="uq_idea_user_like"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    idea_id: int = Field(foreign_key="idea.id")
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)


class IdeaComment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    idea_id: int = Field(foreign_key="idea.id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
