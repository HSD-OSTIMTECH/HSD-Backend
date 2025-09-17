from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlmodel import Session, select

from ..database import engine
from ..models import Form
from ..schemas.forms import FormCreate, FormOut
from datetime import datetime


router = APIRouter(prefix="/forms", tags=["Forms"])


def get_session():
    with Session(engine) as session:
        yield session


@router.post("/", response_model=FormOut)
def create_form(payload: FormCreate, session: Session = Depends(get_session)):
    now = datetime.utcnow()
    new_form = Form(
        title=payload.title,
        description=payload.description,
        status=payload.status or "draft",
        allow_anonymous=payload.allow_anonymous or False,
        created_at=now,
        updated_at=now,
    )
    session.add(new_form)
    session.commit()
    session.refresh(new_form)
    return new_form


@router.get("/", response_model=List[FormOut])
def list_forms(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    session: Session = Depends(get_session),
):
    offset = (page - 1) * page_size
    statement = select(Form).order_by(Form.created_at.desc()).offset(offset).limit(page_size)
    forms = session.exec(statement).all()
    return forms


@router.get("/{form_id}", response_model=FormOut)
def get_form(form_id: int, session: Session = Depends(get_session)):
    form = session.get(Form, form_id)
    if not form:
        raise HTTPException(status_code=404, detail="Form bulunamadı")
    return form



