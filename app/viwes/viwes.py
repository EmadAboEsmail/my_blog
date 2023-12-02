from flask import Blueprint, render_template, redirect, flash, request
from app.models import Post, User
from app import db
from .fields import USER
import mistune

viwe = Blueprint("viwe", __name__)


@viwe.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    pagination = Post.query.order_by(Post.created_at).paginate(page, per_page=2)

    posts = Post.query.order_by(Post.created_at.desc()).all()

    return render_template("index.html", pagination=pagination, posts=posts)


def get_article(article_id):
    article = Post.query.get(article_id)
    return article


def get_user(user_id):
    article = User.query.get(user_id)
    return article


@viwe.route("/markdown")
def markdown():
    markdown_text = """
# Heading

This is an example of converting Markdown to HTML using mistune library.

- Bullet point
- Bullet point
- Bullet point

**Bold text**
_Italic text_
    """

    html = mistune.markdown(markdown_text)
    return render_template("markdown.html", markdown=html)


@viwe.route("/articles/<int:article_id>")
def article(article_id):
    article = get_article(article_id)
    # Highlight article color
    if article:
        article.is_read = True
        db.session.commit()
        flash("تم تحديث حالة القراءة للمنشور بنجاح!", "success")

    # html = mistune.markdown(article.content)
    # user = User.query.filter_by(USER)
    user = get_user(article.user_id)
    return render_template("article.html", user=user, article=article)


@viwe.route("/delete/<int:article_id>")
def delete(article_id):
    article = get_article(article_id)
    db.session.delete(article)
    db.session.commit()
    return redirect("/")


@viwe.route("/edit/<int:id>")
def edit(id):
    article = Post.query.get(id)
    return render_template("edit.html", article=article)


@viwe.route("/profile/<int:user_id>")
def profile(user_id):
    user = get_user(user_id)

    return render_template("profile/profile.html", user=user)
