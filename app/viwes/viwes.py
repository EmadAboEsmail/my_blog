from flask import Blueprint, render_template, url_for, redirect, flash, request
from app.models import Post, User
from app import db
from .fields import USER
import mistune
from app.frames import PostForm

viwe = Blueprint("viwe", __name__)


def get_article(article_id):
    article = Post.query.get(article_id)
    return article


def get_user(user_id):
    user = User.query.get(user_id)
    return user


@viwe.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    pagination = Post.query.order_by(Post.id).paginate(page, per_page=15)

    posts = Post.query.order_by(Post.created_at.desc()).all()

    return render_template("index.html", pagination=pagination, posts=posts)


@viwe.route("/articles/<int:article_id>")
def article(article_id):
    article = get_article(article_id)
    # Highlight article color
    if article:
        article.is_read = True
        db.session.commit()
    text = mistune.html(article.content)

    # html = mistune.markdown(article.content)
    # user = User.query.filter_by(USER)
    user = get_user(article.user_id)
    return render_template("article.html", user=user, article=article, text=text)


@viwe.route("/delete/<int:article_id>")
def delete(article_id):
    article = get_article(article_id)
    db.session.delete(article)
    db.session.commit()
    return redirect("/")


@viwe.route("/edit/<int:id>", methods=["POST", "GET"])
def edit(id):
    form = PostForm()
    post = Post.query.get_or_404(id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post updated.", "success")
        return redirect(f"/articles/{post.id}")
    form.title.data = post.title
    form.content.data = post.content

    return render_template("edit.html", form=form)


@viwe.route("/profile/<int:user_id>")
def profile(user_id):
    user = get_user(user_id)

    return render_template("profile/profile.html", user=user)
