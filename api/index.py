import sys
import os

# Add the root directory to Python path for Vercel
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

# Import the Flask app from the root directory
from app import app

# This is the entry point for Vercel
# Vercel will automatically handle WSGI interface