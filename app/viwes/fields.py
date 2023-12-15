from flask import Blueprint, render_template, redirect, flash, url_for

from app.models import User, Post, Category, Comment
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

from app.frames import LoginForm, SignupForm, PostForm, CategoryForm

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
            flash("من فضلك تاكد من بيانات التسجيل", "ckeck_login")
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

        category = Category.query.get(form.category.data)
        post = Post(
            title=title,
            content=content,
            category=category,
            user_id=int(current_user.id),
        )

        db.session.add(post)
        db.session.commit()
        flash("تم إنشاء المنشور بنجاح!", "chech_'post")
        return redirect("/")

    return render_template("fields/post.html", form=form, name=n)


@fields.route("/category/manage", methods=["GET", "POST"])
@login_required
def manage_category():
    category = Category.query.all()

    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash("تم انشاء الفئة.", "success")
        return redirect(url_for("fields.manage_category"))
    return render_template("fields/man_category.html", form=form, category=category)


@fields.route("/category/<int:category_id>/edit", methods=["GET", "POST"])
@login_required
def edit_category(category_id):
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash("تم تعديل الفئة.", "success")
        return redirect("/category/manage")

    form.name.data = category.name
    return render_template("fields/edit_category.html", form=form)


@fields.route("/category/<int:category_id>/delete", methods=["GET", "POST"])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)

    db.session.delete(category)
    db.session.commit()

    flash("تم حذف الفئة", "delete")
    return redirect("/category/manage")


@fields.route("/category/<string:category>")
def category_posts(category):
    posts = Post.query.filter_by(
        category=Category.query.filter_by(name=category).first()
    ).all()
    return render_template("fields/category.html", category=category, posts=posts)


@fields.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post, comment_form=comment_form)


@fields.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/signup")
