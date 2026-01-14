"""
FastAPI Main Application
-------------------------
Backend API with authentication and chat endpoints.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import timedelta, datetime
from typing import List
import os

from database import get_db, init_db
from models import User, Conversation, ChatMessage
from schemas import (
    UserLogin, UserResponse, Token, TokenData,
    UserCreate, GoogleAuthRequest,
    ConversationCreate, ConversationResponse,
    ChatRequest, ChatMessageResponse, ChatResponse
)
from auth import (
    verify_password, get_password_hash, create_access_token,
    verify_token, ACCESS_TOKEN_EXPIRE_MINUTES
)
from llm_service import llm_instance

# Initialize FastAPI app
app = FastAPI(title="Amzur Chatbot API", version="2.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()
    print("✅ Database initialized")


# Dependency: Get current user
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    username = verify_token(token)
    if username is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    
    return user


# Serve static files (frontend)
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")

# Check if running on Vercel (serverless environment)
IS_VERCEL = os.getenv('VERCEL', '') != ''


# Routes

@app.get("/")
def root():
    """Serve the frontend HTML."""
    if IS_VERCEL:
        # On Vercel, serve from the correct path
        html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "index.html")
    else:
        html_path = os.path.join(frontend_path, "index.html")
    return FileResponse(html_path)


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Amzur Chatbot API v2.0"}


@app.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT token.
    
    - **username**: User's username
    - **password**: User's password
    """
    # Find user by username or email
    user = db.query(User).filter(
        (User.username == form_data.username) | (User.email == form_data.username)
    ).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/signup", response_model=UserResponse)
def signup(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new user account.
    
    - **email**: User's email address
    - **username**: Unique username
    - **password**: User's password
    - **full_name**: Optional full name
    """
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@app.post("/auth/google", response_model=Token)
async def google_auth(
    auth_data: GoogleAuthRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate or create user using Google OAuth.
    """
    try:
        from google.oauth2 import id_token
        from google.auth.transport import requests
        
        # Verify the Google token
        idinfo = id_token.verify_oauth2_token(
            auth_data.credential,
            requests.Request(),
            "479578758374-vk1v6l46q7tpi6vcobho2ljnrdnh2h3j.apps.googleusercontent.com"
        )
        
        # Get user info from Google
        email = idinfo['email']
        name = idinfo.get('name', '')
        google_id = idinfo['sub']
        
        # Check if user exists
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            # Create new user
            username = email.split('@')[0] + '_' + google_id[:6]
            user = User(
                email=email,
                username=username,
                hashed_password=get_password_hash(google_id),  # Use Google ID as password hash
                full_name=name,
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}"
        )


@app.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user


# Conversation Endpoints

@app.get("/conversations", response_model=List[ConversationResponse])
def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all conversations for the current user.
    Returns conversations in reverse chronological order (newest first).
    """
    conversations = db.query(
        Conversation,
        func.count(ChatMessage.id).label('message_count')
    ).outerjoin(
        ChatMessage
    ).filter(
        Conversation.user_id == current_user.id
    ).group_by(
        Conversation.id
    ).order_by(
        Conversation.updated_at.desc()
    ).all()
    
    result = []
    for conv, msg_count in conversations:
        conv_dict = {
            "id": conv.id,
            "title": conv.title,
            "created_at": conv.created_at,
            "updated_at": conv.updated_at,
            "message_count": msg_count
        }
        result.append(conv_dict)
    
    return result


@app.post("/conversations", response_model=ConversationResponse)
def create_conversation(
    conversation: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new conversation."""
    new_conversation = Conversation(
        user_id=current_user.id,
        title=conversation.title
    )
    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)
    
    return {
        "id": new_conversation.id,
        "title": new_conversation.title,
        "created_at": new_conversation.created_at,
        "updated_at": new_conversation.updated_at,
        "message_count": 0
    }


@app.get("/conversations/{conversation_id}/messages", response_model=List[ChatMessageResponse])
def get_conversation_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all messages for a specific conversation."""
    # Verify conversation belongs to user
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = db.query(ChatMessage).filter(
        ChatMessage.conversation_id == conversation_id
    ).order_by(ChatMessage.timestamp).all()
    
    return messages


@app.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a conversation and all its messages."""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    db.delete(conversation)
    db.commit()
    
    return {"message": "Conversation deleted"}


@app.patch("/conversations/{conversation_id}/title")
def update_conversation_title(
    conversation_id: int,
    title: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update conversation title."""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conversation.title = title
    db.commit()
    
    return {"message": "Title updated", "title": title}


# Chat Endpoints

@app.post("/chat", response_model=ChatResponse)
def send_message(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a message and get LLM response.
    
    - Creates new conversation if conversation_id is None
    - Saves user message to database
    - Gets response from Gemini LLM
    - Saves assistant response to database
    - Returns both messages with conversation_id
    """
    conversation_id = chat_request.conversation_id
    
    # Create new conversation if not provided
    if not conversation_id:
        new_conversation = Conversation(
            user_id=current_user.id,
            title="New Chat"
        )
        db.add(new_conversation)
        db.commit()
        db.refresh(new_conversation)
        conversation_id = new_conversation.id
    else:
        # Verify conversation belongs to user
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
    
    # Save user message
    user_message = ChatMessage(
        conversation_id=conversation_id,
        role="user",
        content=chat_request.message
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)
    
    # Auto-generate title from first message
    message_count = db.query(ChatMessage).filter(
        ChatMessage.conversation_id == conversation_id
    ).count()
    
    if message_count == 1:  # First message in conversation
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        # Generate title from first few words
        title_words = chat_request.message.split()[:6]
        conversation.title = " ".join(title_words) + ("..." if len(chat_request.message.split()) > 6 else "")
        db.commit()
    
    # Fetch last 5 exchanges (10 messages) for conversation context
    previous_messages = db.query(ChatMessage).filter(
        ChatMessage.conversation_id == conversation_id,
        ChatMessage.id != user_message.id  # Exclude the current message
    ).order_by(ChatMessage.timestamp.desc()).limit(10).all()
    
    # Reverse to get chronological order
    previous_messages = list(reversed(previous_messages))
    
    # Format conversation history
    conversation_history = [
        {"role": msg.role, "content": msg.content}
        for msg in previous_messages
    ]
    
    # Get LLM response with conversation history
    try:
        llm_response = llm_instance.get_response(chat_request.message, conversation_history)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM Error: {str(e)}"
        )
    
    # Save assistant message
    assistant_message = ChatMessage(
        conversation_id=conversation_id,
        role="assistant",
        content=llm_response
    )
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)
    
    return {
        "conversation_id": conversation_id,
        "user_message": user_message,
        "assistant_message": assistant_message
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
