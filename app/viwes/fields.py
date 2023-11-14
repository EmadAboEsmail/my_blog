from flask import Blueprint, render_template, request, redirect, flash, session
from app.models import User, Post
from app import db, app

from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
    LoginManager,
)
from werkzeug.security import check_password_hash, generate_password_hash

# login_manager = LoginManager(app)
# login_manager.login_view = "login"
fields = Blueprint("fields", __name__)


@fields.route("/login")
def login():

    return render_template("fields/login.html")


@fields.route("/signup", methods=["POST", "GET"])
def signup():
    error = False
    if request.method == "POST":
        user_name = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        isNotUnique = User.query.filter_by(user_name=user_name).first()
        if isNotUnique:
            error = True
        else:
            password = generate_password_hash(password, method="sha256")
            user = User(user_name=user_name, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            # login_user(user, remember=True)

            return redirect()

    return render_template("fields/signup.html", error=error)


@fields.route("/post", methods=["POST", "GET"])
def post():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        tag = request.form.get("tag")
        post = Post(title=title, content=content, tag=tag)
        db.session.add(post)
        db.session.commit()
        return redirect("/")

    return render_template("fields/post.html")


# @fields.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect("/signup")
