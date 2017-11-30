#!/usr/bin/env python
from app import mongo_db


class ExecutionParam(mongo_db.DynamicDocument):
    start_time = mongo_db.DateTimeField(required=True)
    end_time = mongo_db.DateTimeField(required=True)
    page_no = mongo_db.IntField(required=True)
    page_size = mongo_db.IntField(required=True)
    img_url = mongo_db.IntField()               # trade, trade_finished,
    status = mongo_db.IntField()                # trade, trade_finished, transfers, stockin_orders
    process_status = mongo_db.IntField()        # refund, refund_finished,
    order_type = mongo_db.IntField()            # stockin_orders, stockout_orders
    refund_no = mongo_db.StringField()          # refund, refund_finished,
    pd_no = mongo_db.StringField()              # pd
    transfer_no = mongo_db.StringField()        # transfers
    src_refund_no = mongo_db.StringField()      # refund, refund_finished,
    src_order_no = mongo_db.StringField()       # stockout_orders
    warehouse_no = mongo_db.StringField()       # pd, stockout_orders
    from_warehouse_no = mongo_db.StringField()  # transfers
    to_warehouse_no = mongo_db.StringField()    # transfers


class ExecutionPlan(mongo_db.Document):
    meta = {
        "collection": "exec_plan",
        "ordering": ["-exec_time"],
        "strict": False
    }

    type = mongo_db.StringField(required=True)
    exec_time = mongo_db.StringField(required=True)
    handle_flag = mongo_db.BooleanField(required=True)
    params = mongo_db.EmbeddedDocumentField("ExecutionParam")

    def __repr__(self):
        return "<ExecPlan %r--%r>" % (self.type, self.exec_time)
