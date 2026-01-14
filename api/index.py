"""
Vercel Entrypoint for FastAPI Application
-----------------------------------------
This file serves as the entry point for Vercel deployment.
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import the FastAPI app from backend/main.py
from main import app

# This is the entry point that Vercel will use
__all__ = ['app']
