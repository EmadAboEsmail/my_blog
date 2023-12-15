from flask import Blueprint, render_template, url_for, redirect, flash, request
from app.models import Post, User, Comment
from app import db
from .fields import USER
import mistune
from app.frames import PostForm, CommentForm

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


@viwe.route("/articles/<int:article_id>", methods=["POST", "GET"])
def article(article_id):
    article = get_article(article_id)
    # Highlight article color
    form = CommentForm()

    if article:
        article.is_read = True
        db.session.commit()
    text = mistune.html(article.content)
    count = str(text)
    w = count.split(" ")
    len_text = len(w)
    avarage_read = 270
    read = len_text // avarage_read

    # html = mistune.markdown(article.content)
    # user = User.query.filter_by(USER)
    user = get_user(article.user_id)
    return render_template(
        "article.html",
        len_text=len_text,
        user=user,
        article=article,
        text=text,
        form=form,
        read=read,
    )


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


@viwe.route("/articles/<int:article_id>/comments/new", methods=["POST"])
def create_comment(article_id):
    form = CommentForm()

    # if form.validate_on_submit():
    comment = Comment(author=USER.username, body=form.body.data, email=USER.email)
    post = Post.query.get(article_id)
    post.comments.append(comment)
    db.session.commit()
    print("ok --------------")
    return redirect(f"/articles/{post.id}")

    # return redirect("/")


@viwe.route("/articles/<int:article_id>/comments/<int:comment_id>/edit")
def edit_comment(article_id, comment_id):
    form = CommentForm()
    comment = Comment.query.get(comment_id)
    form.body.data = comment.body
    comment.body = form.body.data
    db.session.commit()

    return redirect(url_for("viwe.article", article_id=article_id))


@viwe.route("/articles/<int:article_id>/comments/<int:comment_id>/delete")
def delete_comment(article_id, comment_id):
    comment = Comment.query.get(comment_id)
    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for(".article", article_id=article_id))


@viwe.route("/articles/<int:article_id>/comments/<int:comment_id>")
def show_comment(article_id, comment_id):
    comment = Comment.query.get(comment_id)
    return render_template("article.html", comment=comment)


@viwe.route("/profile/<int:user_id>")
def profile(user_id):
    user = get_user(user_id)
    return render_template("profile/profile.html", user=user)
