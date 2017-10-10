#!/usr/bin/env python
from flask import Blueprint

# 因为 errors 中也引用了 main，因此必须要在下面的 import 之前定义 main。
main = Blueprint("main", __name__)

from . import errors, views
from app.models.user import Permission


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
