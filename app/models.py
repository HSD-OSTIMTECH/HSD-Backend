from sqlmodel import SQLModel, Field
from typing import Optional

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
