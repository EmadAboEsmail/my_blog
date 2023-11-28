from app import db
from flask_login import UserMixin
from datetime import datetime

# from sqlalchemy import ForeignKey


class User(db.Model, UserMixin):
    # __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship("Post", backref="author")


class Post(db.Model):
    # __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # tags = db.relationship(
    # "Tag", secondary="post_tag", backref=db.backref("posts", lazy="dynamic")
    # )
    # comments = db.relationship("Comment", back_populates="post")


# class Tag(db.Model):
#     __tablename__ = "tags"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)


# post_tag_table = db.Table(
#     "post_tag",
#     db.Column("post_id", db.Integer, db.ForeignKey("posts.id")),
#     db.Column("tag_id", db.Integer, db.ForeignKey("tags.id")),
# )


# class Comment(db.Model):
#     __tablename__ = "comments"

#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#     post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
