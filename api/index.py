"""
Vercel entry point for FastAPI application
"""
from app.main import app

# Vercel will use this handler
handler = app
