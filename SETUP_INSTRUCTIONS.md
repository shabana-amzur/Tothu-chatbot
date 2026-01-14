# FastAPI Chatbot - Setup Complete! 🎉

## ✅ What's Been Set Up

1. **Backend (FastAPI)** - Python REST API with JWT authentication
2. **Database (PostgreSQL)** - User authentication and chat history storage
3. **LLM Integration** - Google Gemini AI via LangChain
4. **Frontend** - HTML/CSS/JS single-page application

## 🚀 Running the Application

### Start the Backend Server
```bash
cd /Users/ferozshaik/Desktop/Chatbot/backend
source ../venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will run on: **http://localhost:8000**

### Access the Frontend
Open in your browser:
- **Frontend**: `file:///Users/ferozshaik/Desktop/Chatbot/frontend/index.html`
- **Or** navigate directly to: **http://localhost:8000** (the backend serves the frontend)

## 👥 Test User Credentials

Login with these accounts:

**User 1:**
- Username: `shabana`
- Password: `shabbu@123`

**User 2:**
- Username: `john`
- Password: `john123`

## 📁 Project Structure

```
Chatbot/
├── backend/
│   ├── main.py              # FastAPI application with all routes
│   ├── models.py            # Database models (User, ChatMessage)
│   ├── database.py          # Database connection
│   ├── schemas.py           # Pydantic request/response models
│   ├── auth.py              # JWT authentication & password hashing
│   ├── llm_service.py       # Gemini LLM integration via LangChain
│   ├── create_users.py      # Script to create test users
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables
│
├── frontend/
│   └── index.html           # Complete web interface
│
└── venv/                    # Python virtual environment
```

## 🔑 API Endpoints

### Authentication
- `POST /login` - Login and get JWT token

### Chat Operations
- `POST /chat` - Send message and get AI response
- `GET /chats` - Retrieve chat history
- `DELETE /chats` - Clear chat history

### User Info
- `GET /me` - Get current user information

## 🔧 Configuration

All settings are in `backend/.env`:

```env
GOOGLE_API_KEY=AIzaSyDfF6opokn-it-Y8HlnTFZ65-pJLmpy2rg
DATABASE_URL=postgresql://ferozshaik@localhost:5432/chatbot_db
SECRET_KEY=your-secret-key-change-in-production
```

## 🗄️ Database

**PostgreSQL Database:** `chatbot_db`
**Tables:**
- `users` - User accounts with hashed passwords
- `chat_messages` - Chat history linked to users

### Create New Users
```bash
cd /Users/ferozshaik/Desktop/Chatbot/backend
source ../venv/bin/activate
python create_users.py
```

## 🧪 Testing the App

1. **Start the backend** (see above)
2. **Open the frontend** in browser
3. **Login** with test credentials
4. **Send a message** to the chatbot
5. **Check chat history** - messages persist in database

## 📊 Features Implemented

✅ **User Authentication**
- JWT token-based authentication
- Bcrypt password hashing
- Secure login system

✅ **Chat Functionality**
- Real-time chat with Gemini AI
- Persistent chat history in PostgreSQL
- User-specific message storage

✅ **Backend API**
- FastAPI with automatic OpenAPI docs
- CORS enabled for frontend communication
- Proper error handling and validation

✅ **Frontend UI**
- Clean, responsive design
- Real-time message updates
- Token management in localStorage
- Logout functionality

## 🔍 API Documentation

When the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if PostgreSQL is running
brew services list | grep postgresql

# Start PostgreSQL if needed
brew services start postgresql@14
```

### Database connection errors
```bash
# Verify database exists
psql -l | grep chatbot_db

# Create if missing
createdb chatbot_db
```

### Port already in use
```bash
# Kill existing process on port 8000
lsof -ti:8000 | xargs kill -9
```

## 📝 Notes

- The app uses **Python 3.9.6** (consider upgrading to 3.10+ to remove warnings)
- Gemini model: **gemini-2.5-flash-lite**
- Database user: **ferozshaik** (no password required for local connection)
- JWT tokens expire after **24 hours**

## 🎯 Next Steps

1. **Production Deployment**: Update SECRET_KEY in .env
2. **Python Upgrade**: Upgrade to Python 3.10+ to remove deprecation warnings
3. **Add Features**: User registration, message editing, chat export
4. **Security**: Add rate limiting, input validation, HTTPS

---

**Your chatbot is ready to use! Happy chatting! 🚀**
