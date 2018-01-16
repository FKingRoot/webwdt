#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("WEBWDT_SECRET_KEY") or "xd0@69^d8#1cdd9*e4737"
    # 配置请求执行完逻辑之后自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    # 是否需要追踪对象的修改并且发送信号。这需要额外的内存，如果不必要的可以禁用它。
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 启用记录查询统计数字的功能。
    SQLALCHEMY_RECORD_QUERIES = True

    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    # 启用传输层安全（Transport Layer Security，TLS）协议
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    WEBWDT_MAIL_SUBJECT_PREFIX = "[Web_WDT]"
    WEBWDT_MAIL_SENDER = "Web WDT Admin <web_wdt@example.com>"
    WEBWDT_ADMIN = os.environ.get("WEBWDT_ADMIN") or "Marco.Zhang"

    WEBWDT_DATA_PER_PAGE = 50
    WEBWDT_FOLLOWERS_PER_PAGE = 50
    WEBWDT_COMMENTS_PER_PAGE = 30
    # 缓慢查询的阈值设为 0.5 秒。
    WEBWDT_DB_QUERY_TIMEOUT = 0.5
    # 时间段查询的最大跨度
    WEBWDT_QUERY_MAX_DATE_INTERVAL = 30
    # Client 处理的数据量，超过此值转由 Server 处理。
    WEBWDT_QUERY_CLIENT_DATA_COUNT = 1000

    @classmethod
    def init_app(cls, app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DEBUG_TB_ENABLED = False
    # DEBUG_TB_PANELS = ["flask_mongoengine.panels.MongoDebugPanel"]
    SQLALCHEMY_DATABASE_URI = os.environ.get("WEBWDT_DEV_DATABASE_URL") or \
        "postgresql://devuser:engine@192.168.7.150/webwdt_dev"
    # SQLALCHEMY_BINDS = {
    #     "candidate": os.environ.get("WEBWDT_DEV_DATABASE_URL") or \
    #                  "sqlite:///" + os.path.join(base_dir, "data-dev.sqlite")
    # }
    MONGODB_SETTINGS = {
        "db": "wdt",
        # "host": "192.168.7.150",
        "host": "192.168.5.122",
        # "host": "localhost",
        # "port": 27017,
        "port": 28106,
        "username": "devuser",
        # "username": "deployer",
        # 'password': "123"
        "password": "c#d6",
    }
    # CACHE_TYPE = "simple"
    CACHE_TYPE = "null"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("WEBWDT_TEST_DATABASE_URL") or \
        "postgresql://devuser:engine@192.168.7.150/webwdt_test"
    # SQLALCHEMY_BINDS = {
    #     "candidate": os.environ.get("WEBWDT_TEST_DATABASE_URL") or \
    #                  "sqlite:///" + os.path.join(base_dir, "data-test.sqlite")
    # }
    MONGODB_SETTINGS = {
        "db": "wdt",
        "host": "192.168.7.150",
        "port": 27017,
        # 'username': 'webapp',
        # 'password': 'pwd123'
    }
    WTF_CSRF_ENABLED = False
    # 禁用缓存。
    CACHE_TYPE = "null"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("WEBWDT_DATABASE_URL") or \
        "postgresql://devuser:engine@192.168.7.150/webwdt"
    # SQLALCHEMY_BINDS = {
    #     "candidate": os.environ.get("WEBWDT_DATABASE_URL") or \
    #                  "sqlite:///" + os.path.join(base_dir, "data.sqlite")
    # }
    MONGODB_SETTINGS = {
        "db": "wdt",
        "host": "192.168.7.150",
        "port": 27017,
        # 'username': 'webapp',
        # 'password': 'pwd123'
    }

    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = "192.168.7.150"
    CACHE_REDIS_PORT = "6379"
    CACHE_REDIS_PASSWORD = ""
    # Redis 的 db 库 (基于零号索引)。默认是 0。仅用于 RedisCache。
    CACHE_REDIS_DB = "0"

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, "MAIL_USER_NAME", None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, "MAIL_USE_TLS", None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.WEBWDT_MAIL_SENDER,
            toaddrs=[cls.WEBWDT_ADMIN],
            subject=cls.WEBWDT_MAIL_SUBJECT_PREFIX + " Application Error",
            credentials = credentials,
            secure = secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


config = {
    "development": DevelopmentConfig,
    "testing":     TestingConfig,
    "production":  ProductionConfig,
    "default":     DevelopmentConfig
}
