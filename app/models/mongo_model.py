#!/usr/bin/env python
from app import mongo_db


class ExecutionParam(mongo_db.DynamicDocument):
    start_time = mongo_db.DateTimeField(required=True)
    end_time = mongo_db.DateTimeField(required=True)
    page_no = mongo_db.IntField(required=True)
    page_size = mongo_db.IntField(required=True)


class ExecutionPlan(mongo_db.Document):
    meta = {
        "collection": "exec_plan",
        "ordering": ["-exec_time"],
        "strict": False
    }

    type = mongo_db.StringField(required=True)
    exec_time = mongo_db.DateTimeField(required=True)
    handle_flag = mongo_db.BooleanField(required=True)
    params = mongo_db.EmbeddedDocumentField("ExecutionParam")

    def __repr__(self):
        return "<ExecPlan %r--%r>" % (self.type, self.exec_time)
