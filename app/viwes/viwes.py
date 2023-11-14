from flask import Blueprint, render_template, redirect
from app.models import Post
from app import db

viwe = Blueprint("viwe", __name__)


@viwe.route("/")
def index():
    latest_articles = Post.query.all()

    # most_read_articles = get_most_read_articles()
    return render_template(
        "index.html",
        latest_articles=latest_articles,
    )


def get_article(article_id):
    article = Post.query.get(article_id)
    return article


@viwe.route("/articles/<int:article_id>")
def article(article_id):
    article = get_article(article_id)
    return render_template("article.html", article=article)


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
