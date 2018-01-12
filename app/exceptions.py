#!/usr/bin/env python
# -*- coding: utf-8 -*-
# # import the logging library
# import logging
#
# # 在 app 初始化中已经通过 logging.basicConfig 定义了默认的格式，因此下面的设置不需要：
# # # Get an instance of a logger
# # logger = logging.getLogger(__name__)


class AccessDenied(Exception):
    """ Login/password error. No message, no traceback.
    Example: When you try to log with a wrong password."""
    def __init__(self):
        super(AccessDenied, self).__init__("Access denied")
        self.traceback = ("", "", "")
