from app import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(100), unique=True)

    data = db.Column(db.DateTime(timezone=True), default=func.now())
    post = db.relationship("Post")


class Post(db.Model, UserMixin):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    tag = db.Column(db.String())
    # img = db.Column(db.String())
    content = db.Column(db.String())
    data = db.Column(db.DateTime(timezone=True), default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
