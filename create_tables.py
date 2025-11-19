#!/usr/bin/env python3
"""
Script to create database tables in PostgreSQL
Usage: python3 create_tables.py <DATABASE_URL>
Example: python3 create_tables.py "postgresql://user:pass@host/db"
"""
import sys
from sqlalchemy import create_engine

def create_tables(database_url):
    """Create all tables in the database"""
    try:
        print(f"Connecting to database...")
        engine = create_engine(database_url)
        
        print("Importing models...")
        from app.database import Base
        from app.models import User, Lesson, Quiz, Question, Enrollment, QuizSubmission
        
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        
        print("✅ Tables created successfully!")
        print("\nCreated tables:")
        for table in Base.metadata.sorted_tables:
            print(f"  - {table.name}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 create_tables.py <DATABASE_URL>")
        print("\nExample:")
        print('  python3 create_tables.py "postgresql://user:pass@host:5432/database"')
        print("\nOr set DATABASE_URL environment variable:")
        print('  export DATABASE_URL="postgresql://user:pass@host:5432/database"')
        print("  python3 create_tables.py")
        sys.exit(1)
    
    if sys.argv[1] == "env" or sys.argv[1] == "--env":
        import os
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("❌ DATABASE_URL environment variable not set")
            sys.exit(1)
    else:
        database_url = sys.argv[1]
    
    success = create_tables(database_url)
    sys.exit(0 if success else 1)
