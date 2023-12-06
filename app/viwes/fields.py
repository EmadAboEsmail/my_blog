from flask import Blueprint, render_template, redirect, flash
from app.models import User, Post
from app import db, app

import mistune
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
    LoginManager,
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.frames import LoginForm, SignupForm, PostForm

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
fields = Blueprint("fields", __name__)
USER = current_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@fields.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.Email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("من فضلك تاكد من بيانات التسجيل")
            return redirect("/login")
        login_user(user, remember=True)
        return redirect("/")
    return render_template("fields/login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        password = generate_password_hash(password, method="sha256")
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)

        return redirect("/login")

    return render_template("fields/signup.html", form=form)


@fields.route("/post", methods=["POST", "GET"])
def post():
    n = current_user
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        # content = mistune.html(content)

        post = Post(title=title, content=content, user_id=int(current_user.id))

        db.session.add(post)
        db.session.commit()
        flash("تم إنشاء المنشور بنجاح!", "success")
        return redirect("/")

    return render_template("fields/post.html", form=form, name=n)


@fields.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/signup")
