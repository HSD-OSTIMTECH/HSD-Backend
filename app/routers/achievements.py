from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/achievements", tags=["Achievements"])

class Achievement(BaseModel):
    id: int
    user_id: int
    title: str
    description: str

# Geçici başarımlar (sahte veritabanı)
achievements_data = [
    {"id": 1, "user_id": 1, "title": "Hackathon 1.si", "description": "OSTİMTECH Hackathon birinciliği"},
    {"id": 2, "user_id": 1, "title": "Yılın Üyesi", "description": "2025 Yılında en çok katkı sağlayan HSD üyesi"},
    {"id": 3, "user_id": 2, "title": "Topluluk Etkileşimi", "description": "Sunum moderatörlüğü yaptı"},
]

@router.get("/{user_id}", response_model=List[Achievement])
def get_user_achievements(user_id: int):
    return [item for item in achievements_data if item["user_id"] == user_id] 