"""
User Creation Script
--------------------
Script to create test users in the database.
"""

from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import User
from auth import get_password_hash


def create_user(db: Session, username: str, email: str, password: str, full_name: str):
    """Create a new user."""
    # Check if user exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        print(f"❌ User '{username}' already exists")
        return None
    
    # Create user
    hashed_password = get_password_hash(password)
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        full_name=full_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"✅ User '{username}' created successfully")
    return user


if __name__ == "__main__":
    # Initialize database
    init_db()
    
    # Create session
    db = SessionLocal()
    
    try:
        # Create test users
        create_user(
            db,
            username="shabana",
            email="shabana.sheik@amzur.com",
            password="shabbu@123",
            full_name="Shabana Sheik"
        )
        
        create_user(
            db,
            username="john",
            email="john.doe@amzur.com",
            password="john123",
            full_name="John Doe"
        )
        
        print("\n✅ All users created!")
        print("\nTest credentials:")
        print("  Username: shabana | Password: shabbu@123")
        print("  Username: john    | Password: john123")
        
    finally:
        db.close()
