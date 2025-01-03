"""
This module initializes and configures the Flask application for the todo-list API.
It performs the following tasks:
- Creates an instance of the Flask application.
- Configures the application using settings from the Config class.
- Initializes the SQLAlchemy database extension.
- Registers the routes blueprint.
- Creates database tables if they do not exist.
- Runs the application in debug mode if executed as the main module.
"""

# Initialize the Flask app and import routes/models.
from flask import Flask
from models import User, Post, db
from config import Config
from routes import app as routes_blueprint
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy
jwt = JWTManager(app)
db.init_app(app)

# Register the routes blueprint
app.register_blueprint(routes_blueprint)

with app.app_context():
    db.create_all()  # Create tables if they don't exist
    print("Database tables created")
if __name__ == "__main__":
    # Run the Flask application in debug mode if this script is executed directly
    app.run(debug=True)
