"""
CRUD Operations
---------------
Database operations for users and chat messages.
"""

from sqlalchemy.orm import Session
from database.models import User, ChatMessage
import bcrypt
from typing import List, Optional


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


# User CRUD operations
def create_user(db: Session, email: str, username: str, password: str, full_name: str = None) -> User:
    """Create a new user."""
    hashed_password = hash_password(password)
    db_user = User(
        email=email,
        username=username,
        hashed_password=hashed_password,
        full_name=full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get user by username."""
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Authenticate a user."""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# Chat message CRUD operations
def create_message(db: Session, user_id: int, role: str, content: str) -> ChatMessage:
    """Create a new chat message."""
    db_message = ChatMessage(
        user_id=user_id,
        role=role,
        content=content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_user_messages(db: Session, user_id: int) -> List[ChatMessage]:
    """Get all messages for a user, ordered by timestamp."""
    return db.query(ChatMessage).filter(
        ChatMessage.user_id == user_id
    ).order_by(ChatMessage.timestamp).all()


def delete_user_messages(db: Session, user_id: int):
    """Delete all messages for a user."""
    db.query(ChatMessage).filter(ChatMessage.user_id == user_id).delete()
    db.commit()
