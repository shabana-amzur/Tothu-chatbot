# 🤖 Gemini Chatbot - Beginner's Guide

A simple, production-ready chatbot built with Python, LangChain, Google Gemini, and Streamlit. Perfect for beginners getting started with AI development!

## 📋 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation Guide (macOS)](#installation-guide-macos)
- [Getting Your Gemini API Key](#getting-your-gemini-api-key)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [How It Works](#how-it-works)
- [Common Errors and Fixes](#common-errors-and-fixes)
- [Customization](#customization)
- [Learning Resources](#learning-resources)

## ✨ Features

- 💬 **Interactive Chat Interface**: Clean, user-friendly web interface
- 🧠 **Google Gemini AI**: Powered by Google's latest generative AI model
- 📝 **Chat History**: Maintains conversation context throughout the session
- ⚡ **Real-time Responses**: Instant responses with loading indicators
- 🎨 **Modern UI**: Built with Streamlit for a polished look
- 🔒 **Secure**: API keys stored in environment variables
- 🛠️ **Easy to Customize**: Well-commented code for easy modifications

## 🛠️ Tech Stack

- **Python 3.10+**: Programming language
- **LangChain**: Framework for LLM application development
- **Google Gemini (gemini-pro)**: Large Language Model
- **Streamlit**: Web UI framework
- **python-dotenv**: Environment variable management

## 📁 Project Structure

```
Chatbot/
│
├── app.py                      # Main Streamlit application
├── llm/
│   ├── __init__.py            # Makes llm a Python package
│   └── gemini_llm.py          # Gemini LLM wrapper using LangChain
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment variables file
└── README.md                  # This file
```

## 📦 Prerequisites

Before you begin, ensure you have the following installed on your macOS:

1. **Python 3.10 or higher**
   - Check your Python version:
     ```bash
     python3 --version
     ```
   - If not installed, download from [python.org](https://www.python.org/downloads/)

2. **pip** (Python package manager)
   - Usually comes with Python. Check with:
     ```bash
     pip3 --version
     ```

3. **A Google Account** (to get Gemini API key)

## 🚀 Installation Guide (macOS)

Follow these steps carefully:

### Step 1: Open Terminal
- Press `Cmd + Space`, type "Terminal", and press Enter

### Step 2: Navigate to the Project Directory
```bash
cd ~/Desktop/Chatbot
```

### Step 3: Create a Virtual Environment (Recommended)
A virtual environment keeps your project dependencies isolated.

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

After activation, you should see `(venv)` at the beginning of your terminal prompt.

### Step 4: Install Required Packages
```bash
pip install -r requirements.txt
```

This will install all necessary packages:
- streamlit
- langchain
- langchain-google-genai
- google-generativeai
- python-dotenv

**Installation takes 2-3 minutes.** You'll see progress as packages download.

### Step 5: Verify Installation
```bash
pip list
```

You should see all the packages listed in requirements.txt.

## 🔑 Getting Your Gemini API Key

Google Gemini offers a **FREE tier** for developers!

### Steps to Get Your API Key:

1. **Visit Google AI Studio**
   - Go to: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
   - Or search for "Google AI Studio API Key"

2. **Sign In**
   - Use your Google account to sign in

3. **Create API Key**
   - Click on "Create API Key" button
   - Choose "Create API key in new project" (or select existing project)
   - Copy the generated API key immediately

4. **Important Notes**
   - ⚠️ **Never share your API key publicly**
   - ⚠️ **Don't commit it to GitHub or version control**
   - The free tier has generous limits (60 requests per minute)

## ⚙️ Configuration

### Step 1: Create Your .env File

```bash
# Copy the example file to create your .env file
cp .env.example .env
```

### Step 2: Add Your API Key

Open the `.env` file in VS Code or any text editor:

```bash
# Open with VS Code
code .env
```

Replace `your_api_key_here` with your actual Gemini API key:

```
GOOGLE_API_KEY=AIzaSyD9XxXxXxXxXxXxXxXxXxXxXxXxXxXxXx
```

**Save the file** (`Cmd + S` in VS Code).

### Step 3: Verify .env File

Make sure your `.env` file:
- Is in the root `Chatbot` directory
- Contains `GOOGLE_API_KEY=` followed by your actual key
- Has no extra spaces or quotes around the key

## 🎮 Running the Application

### Start the Chatbot

From the `Chatbot` directory with your virtual environment activated:

```bash
streamlit run app.py
```

### What Happens Next:

1. **Terminal Output**: You'll see:
   ```
   You can now view your Streamlit app in your browser.

   Local URL: http://localhost:8501
   Network URL: http://192.168.x.x:8501
   ```

2. **Browser Opens**: Your default browser will automatically open to `http://localhost:8501`

3. **Chatbot Interface**: You'll see the chatbot interface with:
   - Title: "🤖 Gemini Chatbot"
   - Chat input at the bottom
   - Sidebar with information and controls

### Using the Chatbot:

1. **Type your message** in the chat input at the bottom
2. **Press Enter** or click the send icon
3. **Wait for response** (you'll see a "Thinking..." spinner)
4. **View the response** from Gemini
5. **Continue the conversation** - chat history is maintained

### Stopping the Application:

- Press `Ctrl + C` in the terminal to stop the server
- Close the browser tab

## 🔍 How It Works

### Application Flow:

1. **User Input**: You type a message in the Streamlit UI
2. **Message Stored**: Your message is added to session state (chat history)
3. **LLM Call**: The `GeminiLLM` class sends your message to Google Gemini via LangChain
4. **API Request**: LangChain makes an API call to Google's servers
5. **Response Generation**: Gemini processes your input and generates a response
6. **Display**: The response is displayed in the chat interface
7. **History Update**: Both messages are saved in session state

### Key Components:

#### app.py
- **Streamlit UI**: Creates the web interface
- **Session State**: Maintains chat history across interactions
- **User Input Handling**: Processes user messages
- **Response Display**: Shows Gemini's responses

#### llm/gemini_llm.py
- **GeminiLLM Class**: Wrapper for Gemini model
- **Initialization**: Sets up LangChain's ChatGoogleGenerativeAI
- **get_response()**: Sends messages to Gemini and returns responses
- **Error Handling**: Catches and reports API errors

## 🐛 Common Errors and Fixes

### Error 1: "GOOGLE_API_KEY not found"

**Cause**: The `.env` file is missing or the API key is not set.

**Fix**:
```bash
# Make sure .env file exists
ls -la .env

# If not, create it from example
cp .env.example .env

# Edit and add your API key
code .env
```

### Error 2: "ModuleNotFoundError: No module named 'streamlit'"

**Cause**: Packages not installed or virtual environment not activated.

**Fix**:
```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall packages
pip install -r requirements.txt
```

### Error 3: "API key not valid"

**Cause**: Invalid or incorrect API key.

**Fix**:
1. Go back to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Update your `.env` file with the new key
4. Restart the application

### Error 4: "Port 8501 is already in use"

**Cause**: Another Streamlit app is running.

**Fix**:
```bash
# Kill the existing process
pkill -f streamlit

# Or run on a different port
streamlit run app.py --server.port 8502
```

### Error 5: "429 Resource has been exhausted"

**Cause**: You've hit the API rate limit.

**Fix**:
- Wait a few minutes before trying again
- The free tier has limits: 60 requests per minute
- Consider reducing request frequency

### Error 6: Python command not found

**Cause**: Python is not in your PATH or not installed.

**Fix**:
```bash
# Try with python3
python3 --version

# If that works, use python3 instead of python
python3 -m venv venv
```

## 🎨 Customization

### Change the AI Model's Temperature

Temperature controls randomness (0.0 = deterministic, 1.0 = creative):

In [app.py](app.py#L26):
```python
st.session_state.gemini_llm = GeminiLLM(
    model_name="gemini-pro",
    temperature=0.7  # Change this value (0.0 to 1.0)
)
```

### Customize the UI

In [app.py](app.py):
- **Change Title** (line 43): `st.title("Your Title Here")`
- **Modify Description** (line 44-47): Edit the welcome message
- **Add Features**: Streamlit has many components - see [docs](https://docs.streamlit.io/)

### Add System Prompts

To give the chatbot a personality, modify [llm/gemini_llm.py](llm/gemini_llm.py):

```python
def get_response(self, user_input):
    # Add a system prompt
    system_prompt = "You are a helpful coding assistant."
    full_prompt = f"{system_prompt}\n\nUser: {user_input}"
    
    response = self.llm.invoke(full_prompt)
    return response.content
```

### Change the Model

Google offers different Gemini models. In [llm/gemini_llm.py](llm/gemini_llm.py):

```python
# Available models:
# - gemini-pro (default, best for text)
# - gemini-pro-vision (for images + text)

self.llm = ChatGoogleGenerativeAI(
    model="gemini-pro",  # Change model here
    temperature=0.7,
    google_api_key=self.api_key
)
```

## 📚 Learning Resources

### For Beginners:

- **Python Basics**: [Python.org Tutorial](https://docs.python.org/3/tutorial/)
- **Streamlit**: [Streamlit Documentation](https://docs.streamlit.io/)
- **LangChain**: [LangChain Quickstart](https://python.langchain.com/docs/get_started/quickstart)
- **Gemini API**: [Google AI Documentation](https://ai.google.dev/docs)

### Next Steps:

1. **Add Conversation Memory**: Implement proper conversation history with LangChain
2. **Add RAG (Retrieval Augmented Generation)**: Let the chatbot answer questions about your documents
3. **Deploy to Cloud**: Host your chatbot online using Streamlit Cloud or Heroku
4. **Add Authentication**: Protect your chatbot with user login
5. **Integrate More Models**: Try Claude, GPT-4, or other LLMs

## 🤝 Contributing

This is a learning project! Feel free to:
- Add features
- Improve documentation
- Fix bugs
- Share your customizations

## 📝 License

This project is open source and available under the MIT License.

## 💡 Tips for Beginners

1. **Read the Comments**: Every file has detailed comments explaining what each part does
2. **Experiment**: Try changing values and see what happens
3. **Check the Terminal**: Error messages usually tell you what went wrong
4. **Use VS Code**: It has great Python support and debugging tools
5. **Ask for Help**: AI/ML communities are very welcoming to beginners

## 🎯 What You've Learned

By building this project, you've learned:
- ✅ How to structure a Python project
- ✅ Working with APIs and API keys
- ✅ Using environment variables for security
- ✅ Building web UIs with Streamlit
- ✅ Integrating LLMs with LangChain
- ✅ Managing Python dependencies
- ✅ Virtual environment best practices

## 🚀 Ready to Start?

1. Make sure you have Python installed
2. Get your Gemini API key
3. Follow the installation steps
4. Run the chatbot
5. Start experimenting!

**Happy Coding! 🎉**

---

**Questions or Issues?**
- Check the [Common Errors](#common-errors-and-fixes) section
- Review the comments in the code files
- Google the error message - someone has probably solved it before!
