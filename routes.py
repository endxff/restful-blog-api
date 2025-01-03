from flask import Blueprint, request, jsonify
from models import User, db, Post, Category

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    JWTManager,
)

app = Blueprint("routes", __name__)


# Helper function to format User objects as JSON
def user_to_json(user):
    return {
        "id": user.id,
        "username": user.username,
    }


@app.route("/user/register", methods=["POST"])
def register():
    name = request.json.get("name", None)
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User(name=name, username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created"}), 201


@app.route("/user/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = db.session.query(User).filter_by(username=username).one_or_none()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=str(user_to_json(user)))
    return jsonify(access_token=access_token)
    # return jsonify({"msg": "Logged in"}), 200


@app.route("/posts", methods=["GET"])
def posts():
    posts = db.session.query(Post).all()
    return jsonify(
        [
            {
                "id": post.id,
                "title": post.title,
                "subtitle": post.subtitle,
                "content": post.content,
                "user_id": post.user_id,
                "categories": [category.name for category in post.categories],
            }
            for post in posts
        ]
    )


@app.route("/posts/new", methods=["POST"])
@jwt_required()  # This will require a valid access token to be present in the request
def new_post():
    title = request.json.get("title", None)
    subtitle = request.json.get("subtitle", None)
    content = request.json.get("content", None)
    user_id = request.json.get("user_id", None)
    category_names = request.json.get("categories", [])

    post = Post(
        title=title,
        subtitle=subtitle,
        content=content,
        user_id=user_id,
    )

    categories = []
    for name in category_names:
        category = db.session.query(Category).filter_by(name=name).one_or_none()
        if not category:
            category = Category(name=name)
            db.session.add(category)
        categories.append(category)

    post.categories = categories
    db.session.add(post)
    db.session.commit()
    return jsonify({"msg": "Post created"}), 201
