from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from app.models import User
from app.database import engine

router = APIRouter()

@router.post("/users/", response_model=User)
def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@router.get("/users/", response_model=list[User])
def read_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users
