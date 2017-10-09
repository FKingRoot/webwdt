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

    # 邮件相关
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    # 启用传输层安全（Transport Layer Security，TLS）协议
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    FLASKY_MAIL_SUBJECT_PREFIX = "[Web_WDT]"
    FLASKY_MAIL_SENDER = "Web WDT Admin <web_wdt@example.com>"
    FLASKY_ADMIN = os.environ.get("WEBWDT_ADMIN") or "Marco.Zhang"

    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30
    # 缓慢查询的阈值设为 0.5 秒。
    FLASKY_DB_QUERY_TIMEOUT = 0.5

    @classmethod
    def init_app(cls, app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get("WEBWDT_DEV_DATABASE_URL") or \
    #     "sqlite:///" + os.path.join(base_dir, "data-dev.sqlite")
    SQLALCHEMY_DATABASE_URI = os.environ.get("WEBWDT_DEV_DATABASE_URL") or \
        "postgresql://username:password@hostname/database"


class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get("WEBWDT_TEST_DATABASE_URL") or \
    #     "sqlite:///" + os.path.join(base_dir, "data-test.sqlite")
    SQLALCHEMY_DATABASE_URI = os.environ.get("WEBWDT_TEST_DATABASE_URL") or \
        "postgresql://username:password@hostname/database"
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    # SQLALCHEMY_DATABASE_URI = os.environ.get("WEBWDT_DATABASE_URL") or \
    #     "sqlite:///" + os.path.join(base_dir, "data.sqlite")
    SQLALCHEMY_DATABASE_URI = os.environ.get("WEBWDT_DATABASE_URL") or \
        "postgresql://username:password@hostname/database"

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
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + " Application Error",
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
