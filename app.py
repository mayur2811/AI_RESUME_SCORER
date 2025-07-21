import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.engine.url import make_url
from werkzeug.middleware.proxy_fix import ProxyFix

# Load environment variables from .env file if it exists (optional for local dev)
# Vercel automatically provides environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available in serverless environment

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure file uploads
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure the database
db_url = os.environ.get("DATABASE_URL")
if db_url:
    try:
        url_obj = make_url(db_url)
        if url_obj.host and '@' in url_obj.host:
            logging.warning("Malformed database URL detected. Attempting to fix.")
            # The host part seems to contain the user, like user@host.
            # We will split it and use the second part as the correct host.
            _user_in_host, new_host = url_obj.host.split('@', 1)
            url_obj = url_obj._replace(host=new_host)
            db_url = str(url_obj)
            logging.info("Using corrected database URL.")
    except Exception as e:
        logging.error(f"Failed to parse or correct database URL: {e}")

app.config["SQLALCHEMY_DATABASE_URI"] = db_url 
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    try:
        # Import models to ensure tables are created
        import models  # noqa: F401
        db.create_all()
    except Exception as e:
        # Log database initialization error but don't crash the app
        logging.error(f"Database initialization error: {str(e)}")
        # In production, this might be okay if database exists

# Import routes after app initialization
from routes import *  # noqa: F401, E402
