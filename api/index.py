"""
Vercel entry point for FastAPI application
"""
import sys
import os

# Add the parent directory to the path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.main import app
    from mangum import Mangum
    
    # Vercel will use this handler
    handler = Mangum(app, lifespan="off")
    
except Exception as e:
    print(f"Error initializing app: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    raise
