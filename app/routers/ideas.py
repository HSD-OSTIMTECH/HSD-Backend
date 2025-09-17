from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from sqlmodel import Session, select, func

from ..database import engine
from ..models import Idea, IdeaLike, User, IdeaComment
from ..schemas.ideas import (
    IdeaCreate,
    IdeaOut,
    IdeaCommentCreate,
    IdeaCommentOut,
    IdeaListOut,
    IdeaCommentListOut,
)
from datetime import datetime, timezone


router = APIRouter(prefix="/ideas", tags=["Ideas"])


def get_session():
    with Session(engine) as session:
        yield session


@router.post("/", response_model=IdeaOut)
def create_idea(payload: IdeaCreate, session: Session = Depends(get_session)):
    now = datetime.now(timezone.utc)
    idea = Idea(title=payload.title, content=payload.content, created_at=now, updated_at=now)
    session.add(idea)
    session.commit()
    session.refresh(idea)
    # like_count = 0 at creation
    return IdeaOut(
        id=idea.id,
        title=idea.title,
        content=idea.content,
        like_count=0,
        created_at=idea.created_at,
        updated_at=idea.updated_at,
    )


@router.post("/{idea_id}/like")
def like_idea(idea_id: int, user_id: int, session: Session = Depends(get_session)):
    idea = session.get(Idea, idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Fikir bulunamadı")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

    # Idempotent: if like exists, do nothing
    existing = session.exec(
        select(IdeaLike).where(IdeaLike.idea_id == idea_id, IdeaLike.user_id == user_id)
    ).first()
    if existing:
        return {"ok": True}

    like = IdeaLike(idea_id=idea_id, user_id=user_id, created_at=datetime.now(timezone.utc))
    session.add(like)
    session.commit()
    return {"ok": True}


@router.delete("/{idea_id}/like")
def unlike_idea(idea_id: int, user_id: int, session: Session = Depends(get_session)):
    idea = session.get(Idea, idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Fikir bulunamadı")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

    like = session.exec(
        select(IdeaLike).where(IdeaLike.idea_id == idea_id, IdeaLike.user_id == user_id)
    ).first()
    if not like:
        return {"ok": True}

    session.delete(like)
    session.commit()
    return {"ok": True}


@router.get("/", response_model=IdeaListOut)
def list_ideas(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    # Retrieve ideas with like_count using subquery aggregation
    like_counts_subq = select(IdeaLike.idea_id, func.count(IdeaLike.id).label("cnt")).group_by(IdeaLike.idea_id)
    like_counts = {row[0]: row[1] for row in session.exec(like_counts_subq).all()}

    total = session.exec(select(func.count(Idea.id))).one()
    ideas = session.exec(
        select(Idea).order_by(Idea.created_at.desc()).offset(offset).limit(limit)
    ).all()
    results: List[IdeaOut] = []
    for idea in ideas:
        results.append(
            IdeaOut(
                id=idea.id,
                title=idea.title,
                content=idea.content,
                like_count=like_counts.get(idea.id, 0),
                created_at=idea.created_at,
                updated_at=idea.updated_at,
            )
        )
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": results,
    }


# Comments
@router.post("/{idea_id}/comments", response_model=IdeaCommentOut)
def add_comment(
    idea_id: int,
    payload: IdeaCommentCreate,
    user_id: int | None = None,
    session: Session = Depends(get_session),
):
    idea = session.get(Idea, idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Fikir bulunamadı")
    if user_id is not None:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    comment = IdeaComment(
        idea_id=idea_id,
        user_id=user_id,
        content=payload.content,
        created_at=datetime.now(timezone.utc),
    )
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment


@router.get("/{idea_id}/comments", response_model=IdeaCommentListOut)
def list_comments(
    idea_id: int,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    idea = session.get(Idea, idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Fikir bulunamadı")
    total = session.exec(
        select(func.count(IdeaComment.id)).where(IdeaComment.idea_id == idea_id)
    ).one()
    comments = session.exec(
        select(IdeaComment)
        .where(IdeaComment.idea_id == idea_id)
        .order_by(IdeaComment.created_at.desc())
        .offset(offset)
        .limit(limit)
    ).all()
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": comments,
    }


@router.delete("/{idea_id}/comments/{comment_id}")
def delete_comment(
    idea_id: int,
    comment_id: int,
    user_id: int | None = None,
    session: Session = Depends(get_session),
):
    idea = session.get(Idea, idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Fikir bulunamadı")
    comment = session.get(IdeaComment, comment_id)
    if not comment or comment.idea_id != idea_id:
        raise HTTPException(status_code=404, detail="Yorum bulunamadı")
    # optionally enforce ownership when user_id provided
    if user_id is not None and comment.user_id is not None and comment.user_id != user_id:
        raise HTTPException(status_code=403, detail="Bu yorumu silme yetkiniz yok")
    session.delete(comment)
    session.commit()
    return {"ok": True}


