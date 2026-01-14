# 🚀 Complete Setup Guide for Gemini Chatbot

## Prerequisites

### 1. **Python Version**
- **Minimum Required**: Python 3.9.6 (Currently installed)
- **Recommended**: Python 3.10+ (for full compatibility with all libraries)
- **Note**: Python 3.9 has reached end-of-life. Consider upgrading to Python 3.10 or later.

### 2. **System Requirements**
- macOS (confirmed working)
- Internet connection (for API calls to Google Gemini)
- Terminal access

### 3. **Google Gemini API Key**
- You need a valid Google Gemini API key
- Get your API key from: https://makersuite.google.com/app/apikey
- **Your current API key is already configured in `.env` file** ✅

---

## Installation Steps

### Step 1: Verify Python Installation
```bash
python3 --version
```
Should show Python 3.9.6 or higher.

### Step 2: Navigate to Project Directory
```bash
cd /Users/ferozshaik/Desktop/Chatbot
```

### Step 3: Create Virtual Environment (COMPLETED ✅)
```bash
python3 -m venv venv
```

### Step 4: Activate Virtual Environment
```bash
source venv/bin/activate
```

### Step 5: Upgrade pip (COMPLETED ✅)
```bash
pip install --upgrade pip
```

### Step 6: Install Dependencies (COMPLETED ✅)
```bash
pip install -r requirements.txt
```

---

## Installed Packages

All dependencies have been successfully installed:

### Core Framework
- **Streamlit** 1.50.0 - Web UI framework
- **LangChain** 0.3.27 - LLM application framework
- **LangChain Core** 0.3.82 - Core LangChain functionality
- **LangChain Google GenAI** 2.0.10 - Google Gemini integration

### Google AI Libraries
- **google-generativeai** 0.8.6 - Official Google Gemini library
- **google-ai-generativelanguage** 0.6.15 - AI language service
- **google-api-core** 2.29.0 - Google API core functionality
- **google-auth** 2.47.0 - Google authentication

### Utility Libraries
- **python-dotenv** 1.2.1 - Environment variable management
- **pydantic** 2.12.5 - Data validation
- **numpy** 2.0.2 - Numerical computing
- **pandas** 2.3.3 - Data manipulation

---

## Configuration

### Environment Variables
Your `.env` file is already configured with:
```
GOOGLE_API_KEY=AIzaSyAv8su0B8YVXn3Yt4so_GjqFWBwHg5M3bQ
```

**Security Note**: Never commit the `.env` file to version control!

---

## Running the Application

### Start the Chatbot
```bash
streamlit run app.py
```

Or using the full path:
```bash
/Users/ferozshaik/Desktop/Chatbot/venv/bin/streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

---

## Known Issues & Solutions

### Issue 1: Python 3.9 Deprecation Warnings ⚠️
**Problem**: You'll see FutureWarning messages about Python 3.9 being past end-of-life.

**Impact**: The app works fine, but you may not receive future updates for some libraries.

**Solution**: 
```bash
# Recommended: Upgrade to Python 3.10 or later
brew install python@3.10
# Then recreate the virtual environment with the new Python version
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue 2: OpenSSL Warning ⚠️
**Problem**: urllib3 warning about LibreSSL vs OpenSSL.

**Impact**: No functional impact on the chatbot.

**Solution**: Can be ignored, or upgrade to Python 3.10+ which includes newer SSL libraries.

### Issue 3: Package Compatibility (FIXED ✅)
**Problem**: Previous version conflicts between langchain packages.

**Solution**: Updated `requirements.txt` with compatible versions and reinstalled in clean environment.

---

## Project Structure

```
Chatbot/
│
├── app.py                      # Main Streamlit application
├── llm/
│   ├── __init__.py            # Python package initializer
│   └── gemini_llm.py          # Gemini LLM wrapper
├── requirements.txt            # Python dependencies (UPDATED)
├── .env                        # Environment variables (API key)
├── .env.example               # Example environment file
├── README.md                  # Project documentation
├── SETUP_GUIDE.md             # This file
└── venv/                      # Virtual environment (recreated)
```

---

## Testing the Installation

### Test 1: Import LangChain
```bash
python -c "from langchain_google_genai import ChatGoogleGenerativeAI; print('✅ Success')"
```

### Test 2: Test Streamlit
```bash
streamlit --version
```

### Test 3: Run the App
```bash
streamlit run app.py
```

---

## Troubleshooting

### Problem: "ModuleNotFoundError"
**Solution**: Ensure virtual environment is activated:
```bash
source venv/bin/activate
```

### Problem: "GOOGLE_API_KEY not found"
**Solution**: Check your `.env` file exists and contains the API key.

### Problem: App won't start
**Solution**: 
1. Check all dependencies are installed: `pip list`
2. Verify Python version: `python --version`
3. Check for port conflicts: Try `streamlit run app.py --server.port 8502`

---

## Next Steps

1. ✅ **All prerequisites installed**
2. ✅ **Environment configured**
3. ✅ **Dependencies installed and compatible**
4. 🎯 **Ready to run**: Execute `streamlit run app.py`

### Optional Improvements:
- Upgrade to Python 3.10+ for better library support
- Add custom styling to the Streamlit interface
- Implement conversation history persistence
- Add error handling for API rate limits

---

## Support Resources

- **LangChain Documentation**: https://python.langchain.com/docs/
- **Streamlit Documentation**: https://docs.streamlit.io/
- **Google Gemini API**: https://ai.google.dev/docs
- **Project README**: [README.md](README.md)

---

## Summary of Fixes Applied

1. ✅ Identified version compatibility issues with LangChain packages
2. ✅ Updated `requirements.txt` with compatible version ranges
3. ✅ Recreated virtual environment from scratch
4. ✅ Successfully installed all dependencies
5. ✅ Verified imports work correctly
6. ✅ Confirmed `.env` file has API key configured

**Status**: 🎉 **All issues resolved - Ready to use!**
