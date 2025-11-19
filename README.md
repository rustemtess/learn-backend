# JS Academy Backend

A FastAPI backend that powers the JS Academy learning experience with lessons, quizzes, enrollments, and progress tracking stored in SQLite.

## Features

- User registration and authentication via OAuth2 password flow with JWTs
- Lesson CRUD operations with mentor/admin controls
- Student enrollments with progress tracking
- Quiz authoring, delivery, and submission scoring
- SQLite persistence with SQLAlchemy ORM models

## Getting Started

```bash
cd /Users/rustem/Desktop/learn-site/learn_backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. You can explore it interactively at `/docs`.

## Environment Variables

Create a `.env` file to customize secrets:

```
SECRET_KEY=change-me
ACCESS_TOKEN_EXPIRE_MINUTES=120
DATABASE_URL=sqlite:///./jsacademy.db
```

## Project Layout

- `app/main.py` – FastAPI application, routers, CORS setup
- `app/models.py` – SQLAlchemy models for users, lessons, quizzes, enrollments
- `app/schemas.py` – Pydantic schemas for request/response validation
- `app/routers/` – Route modules grouped by feature area
- `app/security.py` – Password hashing and JWT token helpers
- `app/database.py` – Database engine/session utilities

## Running Tests

Formal tests are not yet included. You can manually validate flows using the Swagger UI or HTTP clients like Thunder Client/Postman. Consider adding pytest-based coverage as the backend grows.

