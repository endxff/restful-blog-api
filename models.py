import bcrypt
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password_hash = Column(String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, password):
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_hash.encode("utf-8")
        )

    def __repr__(self):
        return f"<User {self.name}>"


# Association table for the many-to-many relationship between Post and Category
post_category = Table(
    "post_category",
    db.Model.metadata,
    Column("post_id", Integer, ForeignKey("post.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("category.id"), primary_key=True),
)


class Post(db.Model):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    subtitle = Column(String(50), nullable=True)
    content = Column(String(50), nullable=False)
    user_id = Column(Integer, nullable=True)

    # Many-to-many relationship with Category
    categories = relationship(
        "Category", secondary=post_category, back_populates="posts"
    )

    def __repr__(self):
        return f"<Post {self.title}>"


class Category(db.Model):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    # Many-to-many relationship with Post
    posts = relationship("Post", secondary=post_category, back_populates="categories")

    def __repr__(self):
        return f"<Category {self.name}>"
