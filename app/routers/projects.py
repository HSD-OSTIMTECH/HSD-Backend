from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/projects", tags=["Projects"])

class Project(BaseModel):
    id: int
    title: str
    description: str
    technologies: List[str]
    github: str

# Sahte veriler
projects = [
    {
        "id": 1,
        "title": "HSD Resmi Sitesi",
        "description": "OSTİMTECH topluluğu için web platformu.",
        "technologies": ["Next.js", "Tailwind CSS", "TypeScript"],
        "github": "https://github.com/HSD-OSTIMTECH/HSD-Frontend"
    },
    {
        "id": 2,
        "title": "FastAPI Backend",
        "description": "Bu frontendin verilerini sağlayan API sunucusu.",
        "technologies": ["FastAPI", "Pydantic"],
        "github": "https://github.com/HSD-OSTIMTECH/HSD-Backend"
    }
]

@router.get("/", response_model=List[Project])
def list_projects():
    return projects 