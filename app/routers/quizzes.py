from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_active_user
from ..models import Lesson, Question, Quiz, QuizSubmission, User, UserRole
from ..schemas import QuizCreate, QuizRead, QuizSubmissionCreate, QuizSubmissionRead, QuizUpdate

router = APIRouter(prefix="/quizzes", tags=["quizzes"])


def ensure_editor(user: User):
    if user.role not in {UserRole.admin, UserRole.mentor}:
        raise HTTPException(status_code=403, detail="Mentor or admin role required")


@router.post("", response_model=QuizRead, status_code=status.HTTP_201_CREATED)
def create_quiz(
    payload: QuizCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    ensure_editor(current_user)
    lesson = db.query(Lesson).filter(Lesson.id == payload.lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    quiz = Quiz(
        lesson_id=payload.lesson_id,
        title=payload.title,
        description=payload.description,
        duration_minutes=payload.duration_minutes,
    )
    db.add(quiz)
    db.flush()

    for question in payload.questions:
        db.add(
            Question(
                quiz_id=quiz.id,
                prompt=question.prompt,
                choices=question.choices,
                correct_answer=question.correct_answer,
                explanation=question.explanation,
            )
        )

    db.commit()
    db.refresh(quiz)
    return quiz


@router.get("", response_model=list[QuizRead])
def list_all_quizzes(db: Session = Depends(get_db)):
    return db.query(Quiz).all()


@router.get("/lesson/{lesson_id}", response_model=list[QuizRead])
def quizzes_for_lesson(lesson_id: int, db: Session = Depends(get_db)):
    return db.query(Quiz).filter(Quiz.lesson_id == lesson_id).all()


@router.get("/{quiz_id}", response_model=QuizRead)
def read_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


@router.patch("/{quiz_id}", response_model=QuizRead)
def update_quiz(
    quiz_id: int,
    payload: QuizUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    ensure_editor(current_user)
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(quiz, field, value)

    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return quiz


@router.post("/{quiz_id}/submit", response_model=QuizSubmissionRead)
def submit_quiz(
    quiz_id: int,
    payload: QuizSubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    total = len(quiz.questions)
    if total == 0:
        raise HTTPException(status_code=400, detail="Quiz has no questions")

    correct = 0
    responses = {}
    for question in quiz.questions:
        answer = payload.answers.get(question.id)
        responses[question.id] = answer
        if answer and answer == question.correct_answer:
            correct += 1

    score = (correct / total) * 100
    submission = QuizSubmission(
        quiz_id=quiz.id,
        user_id=current_user.id,
        score=score,
        responses=responses,
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission

