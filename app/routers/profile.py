from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/profile", tags=["Profile"])

class Profile(BaseModel):
    id: int
    name: str
    email: str
    role: str
    achievements: List[str]

# Sahte veri
dummy_profile = {
    "id": 1,
    "name": "Halitcan Emir",
    "email": "halitcan@example.com",
    "role": "Frontend Developer",
    "achievements": [
        "Hackathon Birinciliği",
        "HSD Core Team Üyesi",
        "2025 Proje Ödülü"
    ]
}

@router.get("/", response_model=Profile)
def get_user_profile():
    return dummy_profile 