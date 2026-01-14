"""
LangChain Gemini Integration
-----------------------------
Handles LLM calls using LangChain and Google Gemini.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import List, Dict

load_dotenv()


class GeminiLLM:
    """Wrapper for Google Gemini LLM using LangChain."""
    
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=api_key,
            temperature=0.7
        )
    
    def get_response(self, message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """Get response from Gemini with conversation history.
        
        Args:
            message: Current user message
            conversation_history: List of previous messages [{'role': 'user'/'assistant', 'content': '...'}]
        """
        try:
            messages = []
            
            # Add system message
            messages.append(SystemMessage(content="You are a helpful AI assistant. Provide clear, accurate, and helpful responses."))
            
            # Add conversation history
            if conversation_history:
                for msg in conversation_history:
                    if msg['role'] == 'user':
                        messages.append(HumanMessage(content=msg['content']))
                    elif msg['role'] == 'assistant':
                        messages.append(AIMessage(content=msg['content']))
            
            # Add current message
            messages.append(HumanMessage(content=message))
            
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            raise Exception(f"Error getting LLM response: {str(e)}")


# Singleton instance
llm_instance = GeminiLLM()
