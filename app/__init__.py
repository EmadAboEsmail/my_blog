from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from . import config
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_script import Manager

from flask_wtf import CSRFProtect

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return render_template("error_404.html")


app.config.from_object(config.development)
Bootstrap(app)

# print(app.config["SQLALCHEMY_DATABASE_URI"])
db = SQLAlchemy(app)
app.app_context()
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)


csrf = CSRFProtect(app)
# Register the user with Flask-Login

from app.viwes.viwes import viwe
from app.viwes.fields import fields
from app.models import Post, User

# print(app.config["SECRET_KEY"])


app.register_blueprint(viwe)
app.register_blueprint(fields)
