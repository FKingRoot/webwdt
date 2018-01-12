#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from pymongo import ASCENDING, DESCENDING
from flask import (current_app, url_for, request, session, render_template, redirect, make_response, abort, g, jsonify)
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
import flask_excel as excel

from . import main
from .forms import ExecPlanQueryForm, VoucherQueryForm
from app import db, mongo_collection
from app.models.user import Role, User
from app.models.mongo_model import ExecutionPlan, Trade

@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config["WEBWDT_DB_QUERY_TIMEOUT"]:
            current_app.logger.warning(
                "Slow query: %s\nParameters: %s\nDuration: %f\nContext: %s\n"
                % (query.statement,
                   query.parameters,
                   query.duration,
                   query.context)
            )
    return response


@main.route("/shutdown")
def server_shutdown():
    if not current_app.testing:
        abort(404)  # Not Found
    shutdown = request.environ.get("werkzeug.server.shutdown")
    if not shutdown:
        abort(500)  # Internal Server Error
    shutdown()
    return "Shutting down..."


@main.route("/")
# @login_required
def index():
    return render_template("index.html",
                           top_active=None,
                           breadcrumb=["home"])


@main.route("/execplan", methods=["GET", "POST"])
def execplan():
    # import json
    # data = json.loads(request.form.get('data'))
    #获取Get数据
    # variable1 = request.get_json()
    # variable2 = request.get_data()
    # name=request.args.get('name')
    # age=int(request.args.get('age'))
    # 字符串"True"不能直接通过 bool 强转。
    qcc_exectime = (request.args.get("qcc_exectime", "True") == "True")
    start_time = request.args.get("start_time", datetime.utcnow().strftime("%m/%d/%Y"))
    end_time = request.args.get("end_time", datetime.utcnow().strftime("%m/%d/%Y"))
    qcc_biztypes = (request.args.get("qcc_biztypes", "False") == "True")
    biz_types = request.args.getlist("biz_types")# or ["pull_trades"]
    handled = request.args.get("handled", "1")
    page = request.args.get("page", 1, type=int)

    form = ExecPlanQueryForm(qcc_biztypes=qcc_biztypes)
    if form.validate_on_submit():
        qcc_exectime = form.qcc_exectime.data
        start_time = form.qcd_exectime_start.data
        end_time = form.qcd_exectime_end.data
        qcc_biztypes = form.qcc_biztypes.data
        biz_types = form.qcd_biztypes.data
        handled = form.qcd_handled.data
        return redirect(url_for("main.execplan",
                                qcc_exectime=qcc_exectime,
                                start_time=start_time,
                                end_time=end_time,
                                qcc_biztypes=qcc_biztypes,
                                biz_types=biz_types,
                                handled=handled,
                                page=1))

    # Build query parameters.
    params = {
        "exec_time__gte": datetime.strptime(start_time, "%m/%d/%Y").strftime("%Y-%m-%d 00:00:00"),
        "exec_time__lte": datetime.strptime(end_time, "%m/%d/%Y").strftime("%Y-%m-%d 23:59:59"),
    }
    if qcc_biztypes:
        params["type__in"] = biz_types
    elif params.get("type"):
        del params["type__in"]

    if handled == "2":
        params["handle_flag"] = 1
    elif handled == "3":
        params["handle_flag"] = 0
    elif params.get("handle_flag"):
        del params["handle_flag"]

    queryset = ExecutionPlan.objects(**params)

    # import pdb
    # pdb.set_trace()
    # print(queryset._query)
    # queryset.explain()

    pagination = queryset.order_by("-exec_time", "type") \
        .paginate(page=page,
                  per_page=current_app.config["WEBWDT_DATA_PER_PAGE"]
                  )
    exec_plans = pagination.items

    form.qcc_exectime.data = qcc_exectime
    form.qcd_exectime_start.data = start_time
    form.qcd_exectime_end.data = end_time
    form.qcc_biztypes.data = qcc_biztypes
    form.qcd_biztypes.data = biz_types
    form.qcd_handled.data = handled
    return render_template("exec_plan.html",
                           qcc_exectime=qcc_exectime,
                           start_time=start_time,
                           end_time=end_time,
                           qcc_biztypes=qcc_biztypes,
                           biz_types=biz_types,
                           handled=handled,
                           pagination=pagination,
                           exec_plans=exec_plans,
                           form=form,
                           breadcrumb=["home", "execplan"])


@main.route("/execplan/export/xls", methods=["GET"])
def exec_plan_export_xls():
    query_sets = ExecutionPlan.objects[:5]
    if len(query_sets):
        column_names = ['exec_time', 'type']
        return excel.make_response_from_query_sets(query_sets, column_names, "xls", file_name="d:\\test001.xls")
    return render_template("exec_plan.html")


@main.route("/trade", methods=["GET", "POST"])
def trade():
    # 考虑到每个处理逻辑中的（行）数据量的大小不一致，因此对每个处理逻辑都单独设置客户端处理数据行数，默认取全局量。
    client_data_count = 100 or current_app.config["WEBWDT_QUERY_CLIENT_DATA_COUNT"]
    # qcc_logtime = (request.args.get("qcc_logtime", "True") == "True")
    # start_time = request.args.get("start_time", datetime.utcnow().strftime("%m/%d/%Y"))
    # end_time = request.args.get("end_time", datetime.utcnow().strftime("%m/%d/%Y"))
    # handled = request.args.get("handled", "1")

    # if request.method == 'GET':
    #     pass
    # elif request.method == 'POST':
    #     pass
    # qcc_logtime = request.form.get("qcc_logtime", "True")
    # start_time = request.form.get('qcd_logtime_start', datetime.utcnow().strftime("%m/%d/%Y"))
    # end_time = request.form.get('qcd_logtime_end', datetime.utcnow().strftime("%m/%d/%Y"))
    # handled = request.form.get('qcd_handled', "1")

    form = VoucherQueryForm()
    if form.validate_on_submit():
        qcc_logtime = form.qcc_logtime.data
        start_time = form.qcd_logtime_start.data
        end_time = form.qcd_logtime_end.data
        handled = form.qcd_handled.data
        # form.qcc_logtime.data = qcc_logtime
        # form.qcd_logtime_start.data = start_time
        # form.qcd_logtime_end.data = end_time
        # form.qcd_handled.data = handled
        # return redirect(url_for("main.trade",
        #                         qcc_logtime=qcc_logtime,
        #                         start_time=start_time,
        #                         end_time=end_time,
        #                         handled=handled))
        # return redirect(url_for("main.trade"))

        # Build query parameters.
        params = {
            "log_time__gte": datetime.strptime(start_time, "%m/%d/%Y").strftime("%Y-%m-%d 00:00:00"),
            "log_time__lte": datetime.strptime(end_time, "%m/%d/%Y").strftime("%Y-%m-%d 23:59:59"),
        }

        if handled == "2":
            params["handle_flag"] = 1
        elif handled == "3":
            params["handle_flag"] = 0
        elif params.get("handle_flag"):
            del params["handle_flag"]

        data = []
        queryset = Trade.objects(**params).filter(result__trades__1__exists=True)

        # 查看数据量，决定采用client处理还是server处理
        if queryset.count() <= client_data_count:
            # for r in queryset.order_by("-log_time"):
            for r in queryset.order_by("log_time"):
                data.append({
                    "status": r.content_abbr.status,
                    "log_time": r.log_time,
                    "handle_flag": r.handle_flag,
                    "page_size": r.content_abbr.page_size,
                    "page_no": r.content_abbr.page_no,
                    # "total_count": r.result.total_count,
                    "total_count": len(r.result.trades),
                    "start_time": r.content_abbr.start_time,
                    "end_time": r.content_abbr.end_time,
                    "message": r.result.message,
                    "code": r.result.code,
                    "trades": [{
                                   "trade_id": t.trade_id,
                                   "paid": t.paid,
                                   "receiver_name": t.receiver_name,
                                   "created": t.created,
                                   "modified": t.modified,
                                   "goods_count": len(t.goods_list)
                               } for t in r.result.trades]
                })
            return render_template("trade.html",
                                   data=data,
                                   form=form,
                                   exec_mode=1,     # 控制是否执行查询。0 -- 不执行；1 -- Client；2 -- Server
                                   breadcrumb=["home", "trade"])
        else:
            return render_template("trade.html",
                                   data=data,
                                   qcc_logtime=qcc_logtime,
                                   start_time=start_time,
                                   end_time=end_time,
                                   handled=handled,
                                   form=form,
                                   exec_mode=2,     # 控制是否执行查询。0 -- 不执行；1 -- Client；2 -- Server
                                   breadcrumb=["home", "trade"])

    # form.qcc_logtime.data = qcc_logtime
    # form.qcd_logtime_start.data = start_time
    # form.qcd_logtime_end.data = end_time
    # form.qcd_handled.data = handled
    # return render_template("trade.html",
    #                        qcc_logtime=qcc_logtime,
    #                        start_time=start_time,
    #                        end_time=end_time,
    #                        handled=handled,
    #                        form=form,
    #                        breadcrumb=["home", "trade"])
    return render_template("trade.html",
                           data=[],
                           form=form,
                           exec_mode=0,  # 控制是否执行查询。0 -- 不执行；1 -- Client；2 -- Server
                           breadcrumb=["home", "trade"])


# @main.route("/trade/invoice/<int:id>", methods=["GET"])
@main.route("/trade/invoice/<id>", methods=["GET"])
def trade_invoice(id):
    # db.getCollection('trade').find({"result.trades.trade_id": "28320"},{"result.trades.$":1})
    # queryset = Trade.objects(result__trades__trade_id="28320").fields(slice__result__trades=1)
    # MongoEngine 的 fields() 不支持 MongoDB 的 Projection Operators。
    # queryset = Trade.objects(result__trades__trade_id="28320").fields(**{"result__trades__$":1})  # error!
    # MongoEngine 的 exec_js 可以执行 javascript 脚本，可以考虑在 js 脚本中组成 json 数据结构返回。
    # queryset = Trade.objects.exec_js("db.getCollection('trade').find({'result.trades.trade_id': '28320'},{'result.trades.$':1})")
    # 查看 MongoEngine 的执行计划。
    # w = queryset.explain(True)
    # 目前在不支持 Projection Operators 的情况下，只能通过程序完成过滤。
    # queryset = Trade.objects(result__trades__trade_id="28320").fields(result__trades=1)
    query = {"result.trades.trade_id": id}
    queryset = Trade.objects(__raw__=query).fields(result__trades=1)
    inv = None
    for x in queryset:
        for inv in x.result.trades:
            if inv.trade_id == id:
                # inv = y
                break   # trade_id 是唯一标志，只要找到满足条件的一条数据即可。
    if inv:
        return render_template("trade_invoice.html",
                               inv=inv,
                               breadcrumb=["home", "trade", "invoice"])
    else:
        return render_template("404.html"), 404


@main.route("/stock_in", methods=["GET", "POST"])
def stock_in():
    # db.getCollection('stockin_order')
    #   .find({"result.stockin_list": {$exists : true}, "result.stockin_list.0": {$exists:1}})
    pass


@main.route("/stock_out", methods=["GET", "POST"])
def stock_out():
    # db.getCollection('stockout_order')
    #   .find({"result.stockout_list": {$exists : true}, "result.stockout_list.0": {$exists:1}})
    pass


@main.route("/refund", methods=["GET", "POST"])
def refund():
    # db.getCollection('refund')
    #   .find({"result.refunds": {$exists : true}, $where: "this.result.refunds.length>0"})
    # db.getCollection('refund')
    #   .find({"result.refunds": {$exists : true}, "result.refunds.0": {$exists:1}})
    # 不使用 MongoEngine，直接用 pymongo
    client_data_count = 1000 or current_app.config["WEBWDT_QUERY_CLIENT_DATA_COUNT"]

    form = VoucherQueryForm(max_day_interval=180)
    if form.validate_on_submit():
        qcc_logtime = form.qcc_logtime.data
        start_time = form.qcd_logtime_start.data
        end_time = form.qcd_logtime_end.data
        handled = form.qcd_handled.data

        # Build query parameters.
        # x = mongo_db.find({
        #       "$and": [
        #           {"log_time": {"$gte": "2017-09-01 00:00:00"}},
        #           {"log_time": {"$lte": "2017-09-03 23:59:59"}}
        #       ],
        #       "handle_flag": 1,
        #       "result.refunds.0": {"$exists": 1}
        # }).limit(10)
        query_params = {
            "$and": [
                {"log_time": {"$gte": datetime.strptime(start_time, "%m/%d/%Y").strftime("%Y-%m-%d 00:00:00")}},
                {"log_time": {"$lte": datetime.strptime(end_time, "%m/%d/%Y").strftime("%Y-%m-%d 23:59:59")}}
            ],
            "result.refunds.0": {"$exists": 1}
        }

        if handled == "2":
            query_params["handle_flag"] = 1
        elif handled == "3":
            query_params["handle_flag"] = 0
        elif query_params.get("handle_flag"):
            del query_params["handle_flag"]

        data = []
        queryset = mongo_collection.refund.find(query_params)

        # 查看数据量，决定采用client处理还是server处理
        if queryset.count() <= client_data_count:
            # 注意，游标遍历之后会关闭。
            # 可以使用 itertools 的 tee,
            # 把一个迭代器分为n个迭代器, 返回一个元组.默认是两个。
            # 不要在调用 tee() 之后使用原始迭代器 iterable，否则缓存机制可能无法正确工作。
            # from itertools import tee
            #
            # x1, x2 = tee(db.x.find())
            #
            # list(x1)
            # list(x2)
            for r in queryset.sort([
                        ("log_time", ASCENDING),
                        # ("result.total_count", DESCENDING)
                    ]):
                data.append({
                    "process_status": r["content_abbr"]["process_status"],
                    "log_time": r["log_time"],
                    "handle_flag": r["handle_flag"],
                    "page_size": r["content_abbr"]["page_size"],
                    "page_no": r["content_abbr"]["page_no"],
                    "total_count": len(r["result"]["refunds"]),
                    "start_time": r["content_abbr"]["start_time"],
                    "end_time": r["content_abbr"]["end_time"],
                    "message": r["result"]["message"],
                    "code": r["result"]["code"],
                    "refunds": [{
                                   "refund_id": t["refund_id"],
                                   "refund_amount": t["refund_amount"],
                                   "receiver_name": t["receiver_name"],
                                   "refund_time": t["refund_time"],
                                   "modified": t["modified"],
                                   "refund_order_count": len(t["refund_order_list"])
                               } for t in r["result"]["refunds"]]
                })
            return render_template("refund.html",
                                   data=data,
                                   form=form,
                                   exec_mode=1,  # 控制是否执行查询。0 -- 不执行；1 -- Client；2 -- Server
                                   breadcrumb=["home", "trade"])
        else:
            return render_template("refund.html",
                                   data=data,
                                   qcc_logtime=qcc_logtime,
                                   start_time=start_time,
                                   end_time=end_time,
                                   handled=handled,
                                   form=form,
                                   exec_mode=2,  # 控制是否执行查询。0 -- 不执行；1 -- Client；2 -- Server
                                   breadcrumb=["home", "trade"])
    return render_template("refund.html",
                           data=[],
                           form=form,
                           exec_mode=0,  # 控制是否执行查询。0 -- 不执行；1 -- Client；2 -- Server
                           breadcrumb=["home", "trade"])


@main.route("/refund/invoice/<id>", methods=["GET"])
def refund_invoice(id):
    # db.getCollection('refund').find({"result.refunds.refund_id": "1150"},{"result.refunds.$":1})
    # find_one 查找得到的是一个字典；
    # find 查找得到的是一个游标。
    inv = mongo_collection.refund.find_one({"result.refunds.refund_id": id}, {"result.refunds.$": 1})
    if inv:
        return render_template("refund_invoice.html",
                               inv=inv,
                               breadcrumb=["home", "trade", "invoice"])
    else:
        return render_template("404.html"), 404