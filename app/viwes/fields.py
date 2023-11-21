from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    session,
    url_for,
    jsonify,
)
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

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
fields = Blueprint("fields", __name__)
USER = current_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@fields.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash("من فضلك تاكد من بيانات التسجيل")
            return redirect("/login")
        login_user(user, remember=True)
        session["username"] = current_user.username
        return redirect("/")
    return render_template("fields/login.html")


@fields.route("/signup", methods=["POST", "GET"])
def signup():
    error = False
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        isNotUnique = User.query.filter_by(username=username).first()
        if isNotUnique:
            error = True
        else:
            password = generate_password_hash(password, method="sha256")
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return redirect("/")

    return render_template("fields/signup.html", error=error)


@fields.route("/post", methods=["POST", "GET"])
def post():
    n = current_user
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        # author_id = current_user
        # print(current_user.id)
        post = Post(title=title, content=content, user_id=int(current_user.id))
        db.session.add(post)
        db.session.commit()
        return redirect("/")

    return render_template("fields/post.html", name=n)


@fields.route("/logout")
@login_required
def logout():
    # session.pop("username", None)
    logout_user()
    return redirect("/signup")
