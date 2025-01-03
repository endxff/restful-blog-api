import pytest
from config import TestConfig
from flask import Flask
from flask_testing import TestCase
from models import db, User, Post, Category
from routes import app as routes_blueprint
from flask_jwt_extended import create_access_token, JWTManager


# Define the test class
class TestRoutes(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config.from_object(TestConfig)  # Use the test configuration
        db.init_app(app)  # Initialize the database
        app.register_blueprint(routes_blueprint)
        jwt = JWTManager(app)  # Initialize JWTManager
        return app

    def setUp(self):
        with self.app.app_context():
            db.create_all()
            # Add a test user
            user = User(name="Test User", username="testuser")
            user.set_password("testpassword")
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()  # Remove the session
            db.drop_all()  # Drop all tables

    # Test the register route
    def test_register(self):
        response = self.client.post(
            "/user/register",
            json={
                "name": "Test User 2",
                "username": "testuser2",
                "password": "testpassword2",
            },
        )
        assert response.status_code == 201
        assert response.json["msg"] == "User created"

    # Test the login route
    def test_login(self):
        response = self.client.post(
            "/user/login", json={"username": "testuser", "password": "testpassword"}
        )
        assert response.status_code == 200
        assert "access_token" in response.json

    # Test the create post route
    def test_create_post(self):
        login_response = self.client.post(
            "/user/login", json={"username": "testuser", "password": "testpassword"}
        )
        access_token = login_response.json["access_token"]

        response = self.client.post(
            "/posts/new",
            json={
                "title": "Test Post",
                "subtitle": "Test Subtitle",
                "content": "Test Content",
                "user_id": 1,
                "categories": ["Test Category"],
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 201
        assert response.json["msg"] == "Post created"

    # Test Fetching posts
    def test_get_posts(self):
        response = self.client.get("/posts")
        assert response.status_code == 200
        assert isinstance(response.json, list)
