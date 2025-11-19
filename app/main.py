import sys
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings

print("Importing database...", file=sys.stderr)
from .database import Base, engine
print("✓ Database imported", file=sys.stderr)

print("Importing routers...", file=sys.stderr)
from .routers import admin, auth, enrollments, lessons, quizzes, users
print("✓ Routers imported", file=sys.stderr)

# Don't create tables on every import in serverless environment
# Tables should be created using create_tables.py script
# Base.metadata.create_all(bind=engine)

print("Creating FastAPI app...", file=sys.stderr)
app = FastAPI(title=settings.app_name)
print("✓ FastAPI app created", file=sys.stderr)

# CORS middleware configuration
# Parse comma-separated origins from settings
allowed_origins = [origin.strip() for origin in settings.cors_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(lessons.router)
app.include_router(enrollments.router)
app.include_router(quizzes.router)
app.include_router(admin.router)


# Global exception handler to ensure CORS headers are always sent
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


@app.get("/")
def healthcheck():
    return {"status": "ok", "service": settings.app_name}

