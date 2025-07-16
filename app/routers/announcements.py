from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import date

router = APIRouter(prefix="/announcements", tags=["Announcements"])

class Announcement(BaseModel):
    id: int
    title: str
    content: str
    date: date

class AnnouncementCreate(BaseModel):
    title: str
    content: str
    date: date

# Sahte veri tabanı
announcements = [
    {"id": 1, "title": "Hackathon Başladı!", "content": "OSTİMTECH Hackathon'u başladı.", "date": "2025-07-15"},
    {"id": 2, "title": "Toplantı", "content": "Çarşamba günü saat 14:00'te tanıtım toplantısı var.", "date": "2025-07-17"}
]

@router.get("/", response_model=List[Announcement])
def get_announcements():
    return announcements

@router.post("/", response_model=Announcement)
def create_announcement(item: AnnouncementCreate):
    new_id = len(announcements) + 1
    new_item = {"id": new_id, **item.dict()}
    announcements.append(new_item)
    return new_item 