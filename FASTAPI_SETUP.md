# FastAPI Backend Setup Guide

## Project Structure

```
Chatbot/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models.py            # SQLAlchemy models
│   ├── database.py          # Database connection
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication utilities
│   ├── llm_service.py       # LangChain + Gemini integration
│   ├── create_users.py      # User creation script
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables
└── frontend/
    └── index.html           # Simple HTML/JS frontend
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Variables

The `.env` file is already created with your configuration.

### 3. Create Test Users

```bash
cd backend
python create_users.py
```

This creates:
- **Username**: shabana | **Password**: shabbu@123
- **Username**: john | **Password**: john123

### 4. Start the Backend

```bash
cd backend
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will run at: **http://localhost:8000**

### 5. Open Frontend

Simply open `frontend/index.html` in your browser, or use:

```bash
cd frontend
python -m http.server 3000
```

Then visit: **http://localhost:3000**

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Chat Messages Table
```sql
CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_timestamp (user_id, timestamp)
);
```

## API Endpoints

### POST /login
Login and get JWT token.

**Request Body** (form-data):
```
username: string
password: string
```

**Response**:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### GET /chats
Get all chat history for logged-in user.

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
[
  {
    "id": 1,
    "role": "user",
    "content": "Hello",
    "timestamp": "2026-01-12T10:30:00"
  },
  {
    "id": 2,
    "role": "assistant",
    "content": "Hi! How can I help?",
    "timestamp": "2026-01-12T10:30:05"
  }
]
```

### POST /chat
Send message and get response.

**Headers**: 
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

**Request Body**:
```json
{
  "message": "What is Python?"
}
```

**Response**:
```json
{
  "user_message": {
    "id": 3,
    "role": "user",
    "content": "What is Python?",
    "timestamp": "2026-01-12T10:31:00"
  },
  "assistant_message": {
    "id": 4,
    "role": "assistant",
    "content": "Python is...",
    "timestamp": "2026-01-12T10:31:02"
  }
}
```

## Features Implemented

✅ FastAPI backend with proper structure
✅ PostgreSQL database with SQLAlchemy ORM
✅ JWT authentication with password hashing
✅ User login (no signup in API as per requirements)
✅ Chat history storage per user
✅ LangChain + Gemini integration
✅ Load previous chats on login
✅ Store both user and assistant messages
✅ Simple HTML/JS frontend
✅ CORS enabled for frontend
✅ Production-ready code structure

## Testing

1. **Start backend**: `python backend/main.py`
2. **Open frontend**: `frontend/index.html`
3. **Login** with: `shabana` / `shabbu@123`
4. **Chat** and see history persist

All messages are automatically saved and loaded!
