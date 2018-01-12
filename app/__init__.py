#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from pymongo import MongoClient

from config import config
from extensions import (
    lm, bcrypt, moment, mail, debug_toolbar, cache, jsglue
)
from app.exceptions import AccessDenied

# 使用 logging 会停用 werkzeug 自带的 logging.
# # 使用 logging.basicConfig 定义一个默认的格式。
# logging.basicConfig(
#     level=logging.WARN,
#     format="%(asctime)s %(module)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s"
# )

db = SQLAlchemy()
mongo_db = MongoEngine()

# 暴露全局 pymongo 对象
mongo_client = None
mongo_collection = None

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)
    db.init_app(app)
    mongo_db.init_app(app)
    lm.init_app(app)
    bcrypt.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    debug_toolbar.init_app(app)
    cache.init_app(app)
    jsglue.init_app(app)

    # 初始化 pymongo
    mongo_config = config[config_name].MONGODB_SETTINGS
    # if mongo_config.get("username", "") and mongo_config.get("password", ""):
    #     str = "mongodb://{c[username]}:{c[password]}@{c[host]}:{c[port]}/".format(c=mongo_config)
    # else:
    #     str = "mongodb://{c[host]}:{c[port]}/".format(c=mongo_config)

    global mongo_client
    global mongo_collection
    # mongo_client = MongoClient(str)
    # mongo_collection = mongo_client[mongo_config["db"]]
    mongo_client = MongoClient(host=mongo_config["host"], port=mongo_config["port"])
    if mongo_config.get("username", "") and mongo_config.get("password", ""):
        if not mongo_client[mongo_config["db"]].authenticate(
                mongo_config["username"], mongo_config["password"]):
            raise AccessDenied
    mongo_collection = mongo_client[mongo_config["db"]]


    # 注册蓝图
    from app.main import main as blueprint_main
    app.register_blueprint(blueprint_main)

    from .auth import auth as blueprint_auth
    app.register_blueprint(blueprint_auth, url_prefix="/auth")

    return app
