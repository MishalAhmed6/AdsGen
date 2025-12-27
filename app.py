"""
Vercel entrypoint for Flask application.
This file imports the Flask app from web_app/app.py to satisfy Vercel's requirements.
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import the Flask app from web_app
from web_app.app import app

# Export the app for Vercel
__all__ = ['app']

