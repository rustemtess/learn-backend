from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_active_user
from ..models import Enrollment, Lesson, User
from ..schemas import (
    EnrollmentCreate,
    EnrollmentProgressUpdate,
    EnrollmentRead,
)

router = APIRouter(prefix="/enrollments", tags=["enrollments"])


@router.post("", response_model=EnrollmentRead, status_code=status.HTTP_201_CREATED)
def enroll(
    payload: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    lesson = db.query(Lesson).filter(Lesson.id == payload.lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    existing = (
        db.query(Enrollment)
        .filter(
            Enrollment.lesson_id == payload.lesson_id,
            Enrollment.user_id == current_user.id,
        )
        .first()
    )
    if existing:
        return existing

    enrollment = Enrollment(
        user_id=current_user.id,
        lesson_id=payload.lesson_id,
    )
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


@router.get("/me", response_model=list[EnrollmentRead])
def my_enrollments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return (
        db.query(Enrollment)
        .filter(Enrollment.user_id == current_user.id)
        .order_by(Enrollment.last_accessed.desc())
        .all()
    )


@router.patch("/{enrollment_id}", response_model=EnrollmentRead)
def update_progress(
    enrollment_id: int,
    payload: EnrollmentProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.id == enrollment_id,
            Enrollment.user_id == current_user.id,
        )
        .first()
    )
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    enrollment.progress_percent = payload.progress_percent
    enrollment.last_accessed = datetime.utcnow()
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

