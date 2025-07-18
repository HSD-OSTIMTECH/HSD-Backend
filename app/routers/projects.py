from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlmodel import Session, select
from typing import List
from ..models import Project
from ..database import engine
import shutil
import os

router = APIRouter(prefix="/projects", tags=["Projects"])

# Veritabanı oturumu

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/", response_model=List[Project])
def list_projects(session: Session = Depends(get_session)):
    projects = session.exec(select(Project)).all()
    return projects

@router.post("/", response_model=Project)
def create_project(project: Project, session: Session = Depends(get_session)):
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

@router.get("/{project_id}", response_model=Project)
def get_project(project_id: int, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Proje bulunamadı")
    return project

@router.put("/{project_id}", response_model=Project)
def update_project(project_id: int, updated_project: Project, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Proje bulunamadı")
    for key, value in updated_project.dict(exclude_unset=True).items():
        setattr(project, key, value)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

@router.delete("/{project_id}")
def delete_project(project_id: int, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Proje bulunamadı")
    session.delete(project)
    session.commit()
    return {"ok": True}

@router.post("/upload-image")
def upload_image(file: UploadFile = File(...)):
    images_dir = os.path.join(os.path.dirname(__file__), "..", "static", "images")
    images_dir = os.path.abspath(images_dir)
    os.makedirs(images_dir, exist_ok=True)
    file_path = os.path.join(images_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # URL oluştur (örnek: /static/images/filename.jpg)
    url_path = f"/static/images/{file.filename}"
    return {"image_url": url_path} 