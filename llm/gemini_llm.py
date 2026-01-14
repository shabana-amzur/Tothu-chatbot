"""
Gemini LLM Module
-----------------
This module provides a wrapper around Google's Gemini LLM using LangChain.
It handles the initialization and configuration of the Gemini model.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

class GeminiLLM:
    """
    A wrapper class for Google's Gemini LLM using LangChain.
    
    This class initializes and configures the Gemini model with
    the specified parameters and provides a simple interface to
    interact with the model.
    """
    
    def __init__(self, model_name="gemini-2.5-flash-lite", temperature=0.7):
        """
        Initialize the Gemini LLM wrapper.
        
        Args:
            model_name: Name of the Gemini model (default: gemini-2.5-flash-lite)
            temperature: Controls randomness (0.0 to 1.0)
        """
        # Get API key from environment variables
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY not found. Please create a .env file with your API key."
            )
        
        # Initialize the ChatGoogleGenerativeAI wrapper
        # Using gemini-2.5-flash-lite - lightweight and fast
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=temperature
        )
    
    def get_response(self, prompt):
        """
        Get a response from the Gemini model.
        
        Args:
            prompt: User's input message
            
        Returns:
            str: Model's response
        """
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            raise Exception(f"Error getting response from Gemini: {str(e)}")
