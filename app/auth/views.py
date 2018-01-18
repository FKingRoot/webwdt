#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import (current_app, url_for, request, render_template, redirect, flash, make_response, abort)
from flask_login import current_user, login_user, logout_user, login_required
from flask_babel import gettext as _

from . import auth
from .forms import LoginForm
from app.models.user import User


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(username=form.username.data).first()
        # if user and user.verify_password(form.password.data):
        #     login_user(user, remember=form.remember.data)
        #     return redirect(request.args.get("next") or url_for("main.index"))
        flash(_("Invalid username or password."), category="danger")
        flash(_("Succeed login."), category="success")
        flash(_("database not found."), category="warning")
        flash(_("check this information."), category="info")
    return render_template("auth/login.html", form=form)


@auth.route("/forget", methods=["GET", "POST"])
def login_forget():
    return redirect(request.args.get("next") or url_for("main.index"))


@auth.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    flash(_("You have been logged out."), category="info")
    return redirect(url_for("main.index"))
