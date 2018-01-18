#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 禁止由于 flask_cache 的 jinja2ext.py 中使用了 flask.ext.cache 而不是 flask_cache，
# 而造成的 ExtDeprecationWarning。
import warnings
from flask.exthook import ExtDeprecationWarning
warnings.simplefilter("ignore", ExtDeprecationWarning)

from flask_login import LoginManager
from flask_bcrypt import Bcrypt
# 渲染日期和时间。
from flask_moment import Moment
from flask_mail import Mail
from flask_debugtoolbar import DebugToolbarExtension
from flask_cache import Cache
from flask_jsglue import JSGlue
from flask_babel import Babel


lm = LoginManager()
bcrypt = Bcrypt()
moment = Moment()
mail = Mail()
debug_toolbar = DebugToolbarExtension()
cache = Cache()
jsglue = JSGlue()
babel = Babel()

# # # 如果需要为匿名用户实现一些特定的功能，可创建一个继承自 AnonymousUserMixin 的自定义类，并指派给默认的匿名用户。
# # lm.anonymous_user = your_custom_anonymous_user
# lm.login_view = "auth.login"
# lm.login_message = "Please login to access this page."
# lm.login_message_category = "info"
# lm.session_protection = "strong"
