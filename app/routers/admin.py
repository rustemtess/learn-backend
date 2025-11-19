from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_active_user
from ..models import Enrollment, Lesson, Quiz, User, UserRole

router = APIRouter(prefix="/admin", tags=["admin"])


def ensure_admin(user: User):
    if user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin role required")


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    ensure_admin(current_user)
    
    total_users = db.query(User).count()
    total_lessons = db.query(Lesson).count()
    total_quizzes = db.query(Quiz).count()
    total_enrollments = db.query(Enrollment).count()
    
    return {
        "total_users": total_users,
        "total_lessons": total_lessons,
        "total_quizzes": total_quizzes,
        "total_enrollments": total_enrollments
    }


@router.get("/users")
def list_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, le=100)
):
    ensure_admin(current_user)
    
    users = db.query(User).offset(skip).limit(limit).all()
    
    # Add enrollment count for each user
    result = []
    for user in users:
        enrollments_count = db.query(Enrollment).filter(Enrollment.user_id == user.id).count()
        result.append({
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "created_at": user.created_at,
            "enrollments_count": enrollments_count
        })
    
    return result


@router.get("/users/{user_id}/progress")
def get_user_progress(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    ensure_admin(current_user)
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    enrollments = db.query(Enrollment).filter(Enrollment.user_id == user_id).all()
    
    result = []
    for enrollment in enrollments:
        lesson = db.query(Lesson).filter(Lesson.id == enrollment.lesson_id).first()
        result.append({
            "enrollment_id": enrollment.id,
            "lesson_id": lesson.id,
            "lesson_title": lesson.title,
            "progress_percent": enrollment.progress_percent,
            "last_accessed": enrollment.last_accessed
        })
    
    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role
        },
        "enrollments": result,
        "total_enrollments": len(result),
        "average_progress": sum(e.progress_percent for e in enrollments) / len(enrollments) if enrollments else 0
    }


@router.get("/lessons/stats")
def get_lessons_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    ensure_admin(current_user)
    
    lessons = db.query(Lesson).all()
    
    result = []
    for lesson in lessons:
        enrollments_count = db.query(Enrollment).filter(Enrollment.lesson_id == lesson.id).count()
        avg_progress = db.query(func.avg(Enrollment.progress_percent)).filter(
            Enrollment.lesson_id == lesson.id
        ).scalar() or 0
        quizzes_count = db.query(Quiz).filter(Quiz.lesson_id == lesson.id).count()
        
        result.append({
            "id": lesson.id,
            "title": lesson.title,
            "level": lesson.level,
            "duration_minutes": lesson.duration_minutes,
            "is_published": lesson.is_published,
            "enrollments_count": enrollments_count,
            "average_progress": round(float(avg_progress), 2),
            "quizzes_count": quizzes_count
        })
    
    return result
