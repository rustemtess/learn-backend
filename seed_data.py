#!/usr/bin/env python3
"""
Script to seed the database with initial data
Usage: python3 seed_data.py <DATABASE_URL>
"""
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def seed_database(database_url):
    """Seed the database with initial data"""
    try:
        print(f"Connecting to database...")
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        print("Importing models...")
        from app.models import User, Lesson, Quiz, Question, UserRole
        from app.security import get_password_hash
        
        # Check if data already exists
        if db.query(User).count() > 0:
            print("⚠️  Database already has data. Skipping seed.")
            return True
        
        print("Creating admin user...")
        admin = User(
            email="admin@jsacademy.com",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.admin,
            bio="System administrator"
        )
        db.add(admin)
        
        print("Creating sample lessons...")
        lesson1 = Lesson(
            title="JavaScript Basics",
            description="Learn the fundamentals of JavaScript programming",
            content="""# JavaScript Basics

## Introduction
JavaScript is a versatile programming language used for web development.

## Variables
You can declare variables using `let`, `const`, or `var`:

```javascript
let name = "John";
const age = 25;
var city = "New York";
```

## Data Types
JavaScript has several data types:
- String
- Number
- Boolean
- Object
- Array
- Undefined
- Null

## Functions
Functions are reusable blocks of code:

```javascript
function greet(name) {
  return `Hello, ${name}!`;
}
```
""",
            level="beginner",
            duration_minutes=30,
            is_published=True
        )
        db.add(lesson1)
        
        lesson2 = Lesson(
            title="Functions and Scope",
            description="Master JavaScript functions and variable scope",
            content="""# Functions and Scope

## Function Declaration
```javascript
function add(a, b) {
  return a + b;
}
```

## Arrow Functions
```javascript
const multiply = (a, b) => a * b;
```

## Scope
Variables have different scopes: global, function, and block scope.
""",
            level="intermediate",
            duration_minutes=45,
            is_published=True
        )
        db.add(lesson2)
        
        lesson3 = Lesson(
            title="Objects and Arrays",
            description="Work with JavaScript objects and arrays",
            content="""# Objects and Arrays

## Objects
```javascript
const person = {
  name: "Alice",
  age: 30,
  greet() {
    console.log("Hello!");
  }
};
```

## Arrays
```javascript
const fruits = ["apple", "banana", "orange"];
fruits.push("grape");
```
""",
            level="intermediate",
            duration_minutes=40,
            is_published=True
        )
        db.add(lesson3)
        
        db.flush()  # Get IDs for lessons
        
        print("Creating quizzes...")
        quiz1 = Quiz(
            title="JavaScript Basics Quiz",
            description="Test your knowledge of JavaScript fundamentals",
            lesson_id=lesson1.id,
            duration_minutes=15
        )
        db.add(quiz1)
        
        quiz2 = Quiz(
            title="Functions Quiz",
            description="Challenge yourself with functions and scope",
            lesson_id=lesson2.id,
            duration_minutes=20
        )
        db.add(quiz2)
        
        db.flush()  # Get IDs for quizzes
        
        print("Creating questions...")
        # Quiz 1 questions
        q1 = Question(
            quiz_id=quiz1.id,
            prompt="What keyword is used to declare a constant variable in JavaScript?",
            choices=["var", "let", "const", "define"],
            correct_answer="const"
        )
        db.add(q1)
        
        q2 = Question(
            quiz_id=quiz1.id,
            prompt="Which of the following is NOT a primitive data type in JavaScript?",
            choices=["String", "Number", "Array", "Boolean"],
            correct_answer="Array"
        )
        db.add(q2)
        
        q3 = Question(
            quiz_id=quiz1.id,
            prompt="What does the typeof operator return for an array?",
            choices=["array", "object", "list", "Array"],
            correct_answer="object"
        )
        db.add(q3)
        
        # Quiz 2 questions
        q4 = Question(
            quiz_id=quiz2.id,
            prompt="Which keyword is NOT used to declare a function?",
            choices=["function", "arrow", "async", "const"],
            correct_answer="arrow"
        )
        db.add(q4)
        
        q5 = Question(
            quiz_id=quiz2.id,
            prompt="What is the output of: console.log(typeof (() => {}))?",
            choices=["function", "arrow", "object", "undefined"],
            correct_answer="function"
        )
        db.add(q5)
        
        db.commit()
        print("✅ Database seeded successfully!")
        print(f"\nCreated:")
        print(f"  - 1 Admin user (email: admin@jsacademy.com, password: admin123)")
        print(f"  - 3 Lessons")
        print(f"  - 2 Quizzes")
        print(f"  - 5 Questions")
        
        return True
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 seed_data.py <DATABASE_URL>")
        print("\nExample:")
        print('  python3 seed_data.py "postgresql://user:pass@host:5432/database"')
        print("\nOr use environment variable:")
        print('  export DATABASE_URL="postgresql://user:pass@host:5432/database"')
        print("  python3 seed_data.py env")
        sys.exit(1)
    
    if sys.argv[1] == "env" or sys.argv[1] == "--env":
        import os
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("❌ DATABASE_URL environment variable not set")
            sys.exit(1)
    else:
        database_url = sys.argv[1]
    
    success = seed_database(database_url)
    sys.exit(0 if success else 1)
