#!/usr/bin/python3
import sys
import logging
import os

# Add the backend directory to Python path
sys.path.insert(0, '/var/www/hash-identifier/backend')

# Set environment variables
os.environ['FLASK_ENV'] = 'production'

# Import the Flask app
from app import app as application

# Configure logging
logging.basicConfig(
    filename='/var/www/hash-identifier/backend/logs/app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
