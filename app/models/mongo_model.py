#!/usr/bin/env python
from app import mongo_db


class ExecutionPlan(mongo_db.Document):
    meta = {
        "collection": "exec_plan",
        "ordering": ["-exec_time"],
        "strict": False,
    }

    type = mongo_db.StringField(required=True)
    exec_time = mongo_db.DateTimeField(required=True)
    handle_flag = mongo_db.BooleanField(required=True)

    def __repr__(self):
        return "<ExecPlan %r--%r>" % (self.type, self.exec_time)
