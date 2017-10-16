from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField, ValidationError)
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

from app.models.user import User


class LoginForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(1, 64)],
                           render_kw={"placeholder": "Your name"})
    password = PasswordField("Password",
                             validators=[DataRequired(), Length(6, 64)],
                             render_kw={"placeholder": "Your password"})
    remember = BooleanField("Keep me signed in",
                            render_kw={"checked": ""})  # checked="value"
    # submit = SubmitField("Login")




