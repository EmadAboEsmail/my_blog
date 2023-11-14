from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import config
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config.from_object(config.development)
Bootstrap(app)

# print(app.config["SQLALCHEMY_DATABASE_URI"])
db = SQLAlchemy(app)
app.app_context()
migrate = Migrate(app, db)
# إنشاء عمليات ترحيل تلقائيًا
# migrate.init_app(app, db, directory="migrations")
# db.create_all()
from app.viwes.viwes import viwe
from app.viwes.fields import fields
from app.models import Post, User

# print(app.config["SECRET_KEY"])


app.register_blueprint(viwe)
app.register_blueprint(fields)
