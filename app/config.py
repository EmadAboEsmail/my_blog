import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///blog.db"
    # os.environ.get"SQLALCHEMY_DATABASE_URI")
    # SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MAIL_SERVER = "smtp.googlemail.com"
    # MAIL_PORT = 465
    # MAIL_USE_SSL = True
    # MAIL_USERNAME = os.environ.get("EMAIL_USER")
    # MAIL_PASSWORD o== os.environ.get("EMAIL_PASS")


class development(Config):
    BEBUG = True
