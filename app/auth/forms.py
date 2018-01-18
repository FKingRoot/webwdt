#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from flask_babel import gettext as _
from wtforms import (StringField, PasswordField, BooleanField, SubmitField, ValidationError)
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

from app.models.user import User


class LoginForm(FlaskForm):
    username = StringField(_("Username"),
                           validators=[DataRequired(), Length(1, 64)],
                           render_kw={"placeholder": "Your name"})
    password = PasswordField(_("Password"),
                             validators=[DataRequired(), Length(6, 64)],
                             render_kw={"placeholder": "Your password"})
    remember = BooleanField(_("Keep me signed in"),
                            render_kw={"checked": ""})  # checked="value"
    # submit = SubmitField("Login")
