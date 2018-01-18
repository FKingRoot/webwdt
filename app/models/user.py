#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from flask_login import UserMixin, AnonymousUserMixin
from flask_babel import gettext as _

from app import db
from extensions import bcrypt, lm


class Permission:
    OBSERVER   = 0x01    # 0b00000001：观察者 —— 可以查看业务数据内容。
    WATCHMAN   = 0x02    # 0b00000010：看守者 —— 可以查看系统日志信息。
    ANALYZER   = 0x04    # 0b00000100：分析者 —— 可以查看系统执行计划。
    PEEPER     = 0x08    # 0b00001000：窥视者 —— 可以通过API导出所需的数据。
    ADMINISTER = OBSERVER | WATCHMAN | ANALYZER | PEEPER


class Role(db.Model):
    __tablename__ = "t_role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.String(255))
    default = db.Column(db.Boolean, default=False)
    permissions = db.Column(db.Integer)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return "<Role %r>" % self.name


class User(db.Model, UserMixin):
    __tablename__ = "t_user"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(16), nullable=False, index=True)
    last_name = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(User.self).__init__(**kwargs)

    def __repr__(self):
        return "<User: %r -- %r%r>" % (self.name, self.last_name, self.first_name)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    @property
    def password(self):
        raise AttributeError(_("password is not a readable attribute"))

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


# 将 AnonymousUser 设为用户未登录时 current_user 的值。
# 这样程序不用先检查用户是否登录，就能自由调用 current_user.can() 和 current_user.is_administrator()。
lm.anonymous_user = AnonymousUser


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
