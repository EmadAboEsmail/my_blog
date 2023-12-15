from flask_wtf import FlaskForm
from wtforms import (
    PasswordField,
    HiddenField,
    StringField,
    SubmitField,
    TextAreaField,
    SelectField,
)
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, URL
from app.models import User, Post, Category, Comment
from flask_ckeditor import CKEditorField


class LoginForm(FlaskForm):
    Email = StringField("Email", validators=[DataRequired(), Length(min=5, max=20)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class SignupForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=5, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Signup")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    category = SelectField("Category", coerce=int, default=1)

    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [
            (category.id, category.name)
            for category in Category.query.order_by(Category.name).all()
        ]


class CategoryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            print("Name already in use.")


class CommentForm(FlaskForm):
    author = StringField("Name", validators=[DataRequired(), Length(1, 30)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(1, 254)])
    site = StringField("Site", validators=[Optional(), URL(), Length(0, 255)])
    body = TextAreaField("Comment", validators=[DataRequired()])
    submit = SubmitField()


class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()


class LinkForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(1, 30)])
    url = StringField("URL", validators=[DataRequired(), URL(), Length(1, 255)])
    submit = SubmitField()
