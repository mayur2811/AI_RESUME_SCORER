from app import app
import os

# For local development
if __name__ == '__main__':
    # Use environment variable for debug to be safer in production
    is_debug = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    app.run(host='0.0.0.0', port=5000, debug=is_debug)
