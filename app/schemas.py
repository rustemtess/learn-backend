from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field

from .models import UserRole


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.student
    bio: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    role: Optional[UserRole] = None


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LessonBase(BaseModel):
    title: str
    description: str
    content: str
    level: str = "beginner"
    duration_minutes: int = 30
    tags: Optional[List[str]] = None
    is_published: bool = True


class LessonCreate(LessonBase):
    pass


class LessonUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    level: Optional[str] = None
    duration_minutes: Optional[int] = None
    tags: Optional[List[str]] = None
    is_published: Optional[bool] = None


class LessonRead(LessonBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EnrollmentBase(BaseModel):
    lesson_id: int


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentRead(EnrollmentBase):
    id: int
    user_id: int
    progress_percent: float
    last_accessed: datetime

    class Config:
        from_attributes = True


class EnrollmentProgressUpdate(BaseModel):
    progress_percent: float = Field(ge=0, le=100)


class QuestionBase(BaseModel):
    prompt: str
    choices: List[str]
    correct_answer: str
    explanation: Optional[str] = None


class QuestionCreate(QuestionBase):
    pass


class QuestionRead(QuestionBase):
    id: int

    class Config:
        from_attributes = True


class QuizBase(BaseModel):
    lesson_id: int
    title: str
    description: Optional[str] = None
    duration_minutes: int = 10


class QuizCreate(QuizBase):
    questions: List[QuestionCreate]


class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: Optional[int] = None


class QuizRead(QuizBase):
    id: int
    questions: List[QuestionRead]

    class Config:
        from_attributes = True


class QuizSubmissionCreate(BaseModel):
    answers: Dict[int, str]


class QuizSubmissionRead(BaseModel):
    id: int
    quiz_id: int
    user_id: int
    score: float
    submitted_at: datetime
    responses: Dict[int, str]

    class Config:
        from_attributes = True

