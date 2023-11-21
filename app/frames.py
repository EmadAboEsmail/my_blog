from flask_wtf import FlasForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegisterForm(FlasForm):
    email = StringField(label="email", validators=[DataRequired(), Email()])
    uesrname = StringField(label="uesrname", validators=[DataRequired()])
    password = PasswordField(
        label="password", validators=[DataRequired(), Length(min=6)]
    )
    confirm = PasswordField(
        label="confirm", validators=[DataRequired(), EqualTo(fieldname="password")]
    )
    submit = SubmitField(label="Register")
