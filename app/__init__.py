#!/usr/bin/env python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from config import config
from extensions import (
    lm, bcrypt, moment, mail, cache
)

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)
    db.init_app(app)
    lm.init_app(app)
    bcrypt.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    cache.init_app(app)

    # 注册蓝图
    from app.main import main as blueprint_main
    app.register_blueprint(blueprint_main)

    return app
