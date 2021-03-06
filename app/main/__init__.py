#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, current_app

# 因为 errors 中也引用了 main，因此必须要在下面的 import 之前定义 main。
main = Blueprint("main", __name__)

from . import errors, views, data
from app.models.user import Permission


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

@main.app_context_processor
def inject_app_config():
    return dict(AppConfig=current_app.config)
