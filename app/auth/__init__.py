#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, current_app

auth = Blueprint("auth", __name__)

from . import views


@auth.app_context_processor
def inject_app_config():
    return dict(AppConfig=current_app.config)
