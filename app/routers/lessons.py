from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_active_user
from ..models import Lesson, User, UserRole
from ..schemas import LessonCreate, LessonRead, LessonUpdate

router = APIRouter(prefix="/lessons", tags=["lessons"])


def ensure_editor(user: User):
    if user.role not in {UserRole.admin, UserRole.mentor}:
        raise HTTPException(status_code=403, detail="Mentor or admin role required")


@router.get("", response_model=list[LessonRead])
def list_lessons(
    db: Session = Depends(get_db),
    search: Optional[str] = Query(default=None),
    level: Optional[str] = Query(default=None),
    published_only: bool = Query(default=True),
):
    query = db.query(Lesson)
    if search:
        query = query.filter(Lesson.title.ilike(f"%{search}%"))
    if level:
        query = query.filter(Lesson.level == level)
    if published_only:
        query = query.filter(Lesson.is_published.is_(True))
    return query.order_by(Lesson.created_at.desc()).all()


@router.get("/{lesson_id}", response_model=LessonRead)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.post("", response_model=LessonRead, status_code=status.HTTP_201_CREATED)
def create_lesson(
    payload: LessonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    ensure_editor(current_user)
    lesson = Lesson(**payload.model_dump())
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


@router.patch("/{lesson_id}", response_model=LessonRead)
def update_lesson(
    lesson_id: int,
    payload: LessonUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    ensure_editor(current_user)
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(lesson, key, value)

    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


@router.delete("/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    ensure_editor(current_user)
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    db.delete(lesson)
    db.commit()
    return None

