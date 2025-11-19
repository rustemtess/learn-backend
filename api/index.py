"""
Vercel entry point for FastAPI application
"""
import sys
import os

# Add the parent directory to the path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Log environment info for debugging
print(f"Python version: {sys.version}", file=sys.stderr)
print(f"Working directory: {os.getcwd()}", file=sys.stderr)
print(f"DATABASE_URL set: {'DATABASE_URL' in os.environ}", file=sys.stderr)
print(f"SECRET_KEY set: {'SECRET_KEY' in os.environ}", file=sys.stderr)
print(f"CORS_ORIGINS set: {'CORS_ORIGINS' in os.environ}", file=sys.stderr)

try:
    print("Importing app.main...", file=sys.stderr)
    from app.main import app
    print("✓ app.main imported", file=sys.stderr)
    
    print("Importing mangum...", file=sys.stderr)
    from mangum import Mangum
    print("✓ mangum imported", file=sys.stderr)
    
    # Vercel will use this handler
    print("Creating Mangum handler...", file=sys.stderr)
    handler = Mangum(app, lifespan="off")
    print("✓ Handler created successfully", file=sys.stderr)
    
except Exception as e:
    print(f"❌ Error initializing app: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    raise
