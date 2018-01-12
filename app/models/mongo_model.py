#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import mongo_db


class ExecutionParam(mongo_db.DynamicDocument):
    start_time = mongo_db.DateTimeField(required=True, verbose_name="Start Time")
    end_time = mongo_db.DateTimeField(required=True, verbose_name="End time")
    page_no = mongo_db.IntField(required=True, verbose_name="Page No")
    page_size = mongo_db.IntField(required=True, verbose_name="Page Size")
    img_url = mongo_db.IntField(verbose_name="Image URL")                       # trade, trade_finished,
    status = mongo_db.IntField(verbose_name="Status")                           # trade, trade_finished, transfers, stockin_orders
    process_status = mongo_db.IntField(verbose_name="Process Status")           # refund, refund_finished,
    order_type = mongo_db.IntField(verbose_name="Order Type")                   # stockin_orders, stockout_orders
    refund_no = mongo_db.StringField(verbose_name="Refund No")                  # refund, refund_finished,
    pd_no = mongo_db.StringField(verbose_name="PD No")                          # pd
    transfer_no = mongo_db.StringField(verbose_name="Transfer No")              # transfers
    src_refund_no = mongo_db.StringField(verbose_name="Source Refund No")       # refund, refund_finished,
    src_order_no = mongo_db.StringField(verbose_name="Source Order No")         # stockout_orders
    warehouse_no = mongo_db.StringField(verbose_name="Warehouse No")            # pd, stockout_orders
    from_warehouse_no = mongo_db.StringField(verbose_name="From Warehouse No")  # transfers
    to_warehouse_no = mongo_db.StringField(verbose_name="To Warehouse No")      # transfers

    def __repr__(self):
        return "<ExecutionParam %r--%r>" % (self.type, self.exec_time)


class ExecutionPlan(mongo_db.Document):
    meta = {
        "collection": "exec_plan",
        "ordering": ["-exec_time"],
        # 默认情况下，模型中未定义，但存在于保存的数据中的任何额外属性，将会引发一个 FieldDoesNotExist 错误。
        # 通过在 meta 字典中将 strict 设为 False，可以禁用该异常处理。
        "strict": False
    }

    type = mongo_db.StringField(required=True)
    exec_time = mongo_db.StringField(required=True)
    handle_flag = mongo_db.BooleanField(required=True)
    params = mongo_db.EmbeddedDocumentField("ExecutionParam")

    def __repr__(self):
        return "<ExecutionPlan %r--%r>" % (self.type, self.exec_time)


class Goods(mongo_db.EmbeddedDocument):
    tax_rate = mongo_db.StringField()
    goods_id = mongo_db.StringField()
    bind_oid = mongo_db.StringField()
    suite_name = mongo_db.StringField()
    num = mongo_db.StringField()
    spec_no = mongo_db.StringField()
    modified = mongo_db.StringField()
    refund_num = mongo_db.StringField()
    goods_type = mongo_db.StringField()
    goods_no = mongo_db.StringField()
    trade_id = mongo_db.StringField()
    share_price = mongo_db.StringField()
    src_tid = mongo_db.StringField()
    rec_id = mongo_db.StringField()
    suite_num = mongo_db.StringField()
    api_goods_name = mongo_db.StringField()
    delivery_term = mongo_db.StringField()
    commission = mongo_db.StringField()
    src_oid = mongo_db.StringField()
    goods_name = mongo_db.StringField()
    adjust = mongo_db.StringField()
    suite_id = mongo_db.StringField()
    prop2 = mongo_db.StringField()
    share_post = mongo_db.StringField()
    discount = mongo_db.StringField()
    spec_name = mongo_db.StringField()
    created = mongo_db.StringField()
    large_type = mongo_db.StringField()
    invoice_content = mongo_db.StringField()
    api_spec_name = mongo_db.StringField()
    guarantee_mode = mongo_db.StringField()
    remark = mongo_db.StringField()
    weight = mongo_db.StringField()
    cid = mongo_db.StringField()
    platform_id = mongo_db.StringField()
    from_mask = mongo_db.StringField()
    suite_amount = mongo_db.StringField()
    share_amount = mongo_db.StringField()
    invoice_type = mongo_db.StringField()
    spec_code = mongo_db.StringField()
    order_price = mongo_db.StringField()
    actual_num = mongo_db.StringField()
    price = mongo_db.StringField()
    suite_discount = mongo_db.StringField()
    suite_no = mongo_db.StringField()
    spec_id = mongo_db.StringField()
    refund_status = mongo_db.StringField()
    gift_type = mongo_db.StringField()
    paid = mongo_db.StringField()

    def __repr__(self):
        return "<Goods %r--%r>" % (self.spec_no, self.goods_name)


class TradeItem(mongo_db.EmbeddedDocument):
    meta = {
        "strict": False
    }

    profit = mongo_db.StringField()
    invoice_id = mongo_db.StringField()
    tax_rate = mongo_db.StringField()
    warehouse_no = mongo_db.StringField()
    goods_list = mongo_db.ListField(mongo_db.EmbeddedDocumentField(Goods))
    remark_flag = mongo_db.StringField()
    goods_cost = mongo_db.StringField()
    platform_id = mongo_db.StringField()
    receiver_address = mongo_db.StringField()
    stockout_no = mongo_db.StringField()
    version_id = mongo_db.StringField()
    receiver_dtb = mongo_db.StringField()
    discount = mongo_db.StringField()
    invoice_title = mongo_db.StringField()
    modified = mongo_db.StringField()
    fenxiao_nick = mongo_db.StringField()
    id_card_type = mongo_db.StringField()
    shop_name = mongo_db.StringField()
    flag_name = mongo_db.StringField()
    raw_goods_count = mongo_db.StringField()
    goods_count = mongo_db.StringField()
    logistics_type = mongo_db.StringField()
    invoice_content = mongo_db.StringField()
    logistics_id = mongo_db.StringField()
    fchecker_id = mongo_db.StringField()
    print_remark = mongo_db.StringField()
    id_card = mongo_db.StringField()
    receiver_mobile = mongo_db.StringField()
    trade_id = mongo_db.StringField()
    handle_flag = mongo_db.StringField()
    checker_id = mongo_db.StringField()
    trade_from = mongo_db.StringField()
    customer_no = mongo_db.StringField()
    post_amount = mongo_db.StringField()
    salesman_name = mongo_db.StringField()
    receiver_name = mongo_db.StringField()
    checker_name = mongo_db.StringField()
    goods_type_count = mongo_db.StringField()
    receiver_province = mongo_db.StringField()
    receiver_ring = mongo_db.StringField()
    paid = mongo_db.StringField()
    goods_amount = mongo_db.StringField()
    pay_account = mongo_db.StringField()
    ext_cod_fee = mongo_db.StringField()
    trade_type = mongo_db.StringField()
    split_package_num = mongo_db.StringField()
    shop_no = mongo_db.StringField()
    currency = mongo_db.StringField()
    logistics_name = mongo_db.StringField()
    dap_amount = mongo_db.StringField()
    logistics_no = mongo_db.StringField()
    consign_status = mongo_db.StringField()
    salesman_id = mongo_db.StringField()
    warehouse_type = mongo_db.StringField()
    receiver_district = mongo_db.StringField()
    buyer_message = mongo_db.StringField()
    single_spec_no = mongo_db.StringField()
    delivery_term = mongo_db.StringField()
    commission = mongo_db.StringField()
    src_tids = mongo_db.StringField()
    receiver_city = mongo_db.StringField()
    trade_time = mongo_db.StringField()
    refund_status = mongo_db.StringField()
    fenxiao_type = mongo_db.StringField()
    receivable = mongo_db.StringField()
    receiver_zip = mongo_db.StringField()
    shop_remark = mongo_db.StringField()
    created = mongo_db.StringField()
    receiver_area = mongo_db.StringField()
    freeze_reason = mongo_db.StringField()
    weight = mongo_db.StringField()
    bad_reason = mongo_db.StringField()
    trade_status = mongo_db.StringField()
    receiver_telno = mongo_db.StringField()
    checkouter_id = mongo_db.StringField()
    trade_no = mongo_db.StringField()
    invoice_type = mongo_db.StringField()
    cod_amount = mongo_db.StringField()
    raw_goods_type_count = mongo_db.StringField()
    pay_time = mongo_db.StringField()
    other_amount = mongo_db.StringField()
    post_cost = mongo_db.StringField()
    to_deliver_time = mongo_db.StringField()
    logistics_code = mongo_db.StringField()
    buyer_nick = mongo_db.StringField()
    cs_remark = mongo_db.StringField()
    tax = mongo_db.StringField()

    def __repr__(self):
        return "<TradeItem %r--%r>" % (self.trade_no, self.receiver_name)


class ContentAbbr(mongo_db.DynamicDocument):
    start_time = mongo_db.DateTimeField(required=True)
    end_time = mongo_db.DateTimeField(required=True)
    page_no = mongo_db.IntField(required=True)
    page_size = mongo_db.IntField(required=True)
    img_url = mongo_db.IntField()   # trade, trade_finished,
    status = mongo_db.IntField()    # trade, trade_finished, transfers, stockin_orders

    def __repr__(self):
        return "<ContentAbbr %r--%r>" % (self.start_time, self.end_time)


class Result(mongo_db.EmbeddedDocument):
    total_count = mongo_db.StringField()
    message = mongo_db.StringField()
    code = mongo_db.StringField()
    trades = mongo_db.ListField(mongo_db.EmbeddedDocumentField(TradeItem))

    def __repr__(self):
        return "<Result %r--%r>" % (self.total_count, self.code)


class Trade(mongo_db.Document):
    meta = {
        "collection": "trade",
        # "ordering": ["-log_time"],  # 如果指明排序，有可能出现排序操作使用超过预设的32M内存限制的错误。
        "strict": False
    }

    log_time = mongo_db.StringField(required=True)
    handle_flag = mongo_db.BooleanField(required=True)
    content_abbr = mongo_db.EmbeddedDocumentField("ContentAbbr")
    result = mongo_db.EmbeddedDocumentField(Result)

    def __repr__(self):
        return "<Trade %r--%r>" % (self.log_time, self.result)

    def __str__(self):
        return self.__repr__()
