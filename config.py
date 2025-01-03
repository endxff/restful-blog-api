# Store database configurations for SQLAlchemy, including the database URI and track modifications setting.
import os

# Define the base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    JWT_SECRET_KEY = "super-secret"
    # The database URI that should be used for the connection.
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///database.db")
    # Disable Flask-SQLAlchemy event system to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
