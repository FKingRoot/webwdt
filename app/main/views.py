#!/usr/bin/env python
from datetime import datetime
from flask import (current_app, url_for, request, session, render_template, redirect, make_response, abort, g, jsonify)
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
import flask_excel as excel

from . import main
from .forms import ExecPlanQueryForm, VoucherQueryForm
from app import db
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
    qcc_logtime = (request.args.get("qcc_logtime", "True") == "True")
    start_time = request.args.get("start_time", datetime.utcnow().strftime("%m/%d/%Y"))
    end_time = request.args.get("end_time", datetime.utcnow().strftime("%m/%d/%Y"))
    handled = request.args.get("handled", "1")
    # page = request.args.get("page", 1, type=int)

    form = VoucherQueryForm()
    if form.validate_on_submit():
        qcc_logtime = form.qcc_logtime.data
        start_time = form.qcd_logtime_start.data
        end_time = form.qcd_logtime_end.data
        handled = form.qcd_handled.data
        return redirect(url_for("main.trade",
                                qcc_logtime=qcc_logtime,
                                start_time=start_time,
                                end_time=end_time,
                                handled=handled,
                                page=1))

    # # Build query parameters.
    # params = {
    #     "log_time__gte": datetime.strptime(start_time, "%m/%d/%Y").strftime("%Y-%m-%d 00:00:00"),
    #     "log_time__lte": datetime.strptime(end_time, "%m/%d/%Y").strftime("%Y-%m-%d 23:59:59"),
    # }
    #
    # if handled == "2":
    #     params["handle_flag"] = 1
    # elif handled == "3":
    #     params["handle_flag"] = 0
    # elif params.get("handle_flag"):
    #     del params["handle_flag"]

    # 如果要查询数组长度是否大于 20：
    # posts = Post.objects.filter(__raw__={'$where': 'this.likes.length > 20'})
    # 或者判断是否存在第 21 个元素（该方式只能运行在 MongoDB 2.2+）：
    # posts = Post.objects.filter(likes__21__exists=True)
    # queryset = Trade.objects(**params).filter(__raw__={"$where": "this.result.trades.length>0"})
    # queryset = Trade.objects(**params).filter(result__trades__1__exists=True).limit(3)  # OK!!!
    # queryset = Trade.objects(**params).filter(result__trades__1__exists=True)
    # from bson.son import SON
    # queryset = Trade.objects(**params).filter(result__trades__1__exists=True)\
    #     .aggregate([{"$sort": SON([("log_time", -1)])}], allowDiskUse=True)
    # x = len(queryset)
    #
    # pagination = queryset.order_by("-log_time") \
    #     .paginate(page=page,
    #               per_page=current_app.config["WEBWDT_DATA_PER_PAGE"]
    #               )
    # exec_plans = pagination.items

    form.qcc_logtime.data = qcc_logtime
    form.qcd_logtime_start.data = start_time
    form.qcd_logtime_end.data = end_time
    form.qcd_handled.data = handled
    return render_template("trade.html",
                           qcc_logtime=qcc_logtime,
                           start_time=start_time,
                           end_time=end_time,
                           handled=handled,
                           # pagination=pagination,
                           # exec_plans=exec_plans,
                           form=form,
                           breadcrumb=["home", "trade"])


@main.route("/trade/data", methods=["GET", "POST"])
# def trade_data(start_time, end_time, handled):
def trade_data():
    # 定义列名
    CONST_COLS = ["#", "content_abbr.status", "log_time", "handle_flag", "content_abbr.page_size", "content_abbr.page_no", "result.trades.length",#"result.total_count",
                  "content_abbr.start_time", "content_abbr.end_time", "result.message", "result.code"]

    # 自定义参数
    start_time = request.form.get("ajax_start_time")
    end_time = request.form.get("ajax_end_time")
    handled = request.form.get("ajax_handled")

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

    ####
    # DataTables 发送到服务器的参数
    #
    # 绘制计数器。这个是用来确保Ajax从服务器返回的是对应的（Ajax是异步的，因此返回的顺序是不确定的）。 要求在服务器接收到此参数后再返回。
    front_dt_draw = request.form.get("draw")
    # 分页的第一条数据的起始位置，0代表第一条数据。
    front_dt_start = request.form.get("start")
    # 告诉服务器每页显示的条数，这个数字会等于返回的 data集合的记录数，可能会大于因为服务器可能没有那么多数据。这个也可能是-1，代表需要返回全部数据。
    front_dt_length = request.form.get("length")
    # 全局的搜索条件，条件会应用到每一列（searchable需要设置为true）。
    front_dt_search_val = request.form.get("search[value]")
    # 如果为 true代表全局搜索的值是作为正则表达式处理，为 false则不是。 注意：通常在服务器模式下对于大数据不执行这样的正则表达式，但这都是自己决定的。
    front_dt_search_regx = request.form.get("search[regex]")
    # front_dt_column_cnt = request.form.get("col_cnt") # 自定义参数
    # order[i][column]
    # order[i][dir]

    # db.trade.createIndex({"log_time": -1})
    filter_params = ""
    order_params = []
    for x in range(len(CONST_COLS)):
        ord_idx = request.form.get("order["+str(x)+"][column]")
        ord_dir = request.form.get("order["+str(x)+"][dir]")
        if ord_idx and ord_dir:
            order_params.append(("-" if ord_dir.lower() == "desc" else "") + CONST_COLS[int(ord_idx)])

    #t = Trade.objects(**({'log_time__gte': '2017-06-01 00:00:00', 'log_time__lte': '2017-06-25 23:59:59', 'handle_flag': 1})).order_by("-log_time","handle_flag").limit(50)
    queryset = Trade.objects(**params).filter(result__trades__1__exists=True).order_by(*order_params)
    # sql_txt = """SELECT '', *
    #              FROM tbl_purchaseinfo """\
    #           + ("""ORDER BY """ + order_params if order_params else """""")\
    #           + """ LIMIT(""" + front_dt_length + """)
    #                OFFSET """ + front_dt_start + """;"""
    # res = db.session.execute(sql_txt).fetchall()

    ####
    # 服务器需要返回的数据
    #
    back_dt = {
        # 必要！Datatables发送的draw是多少，则服务器返回多少。
        # 注意！！！出于安全的考虑，强烈要求把这个转换为整形，即数字后再返回，而不是纯粹的接受然后返回，目的是防止跨站脚本（XSS）攻击。
        "draw": int(front_dt_draw),
        # 必要！即没有过滤的记录数（数据库里总共记录数）。
        "recordsTotal": queryset.count()
    }
    # 必要！过滤后的记录数（如果有接收到前台的过滤条件，则返回的是过滤后的记录数）。
    back_dt["recordsFiltered"] = back_dt["recordsTotal"]
    # 必要！表中中需要显示的数据。这是一个对象数组，也可以只是数组。
    # 区别在于：纯数组前台无需用 columns 绑定数据，会自动按照顺序去显示；对象数组则需要用 columns 绑定数据才能正常显示。
    back_dt_data = []
    # from itertools import islice
    # res = islice(queryset, int(front_dt_start), int(front_dt_length))
    # x = queryset.count()
    # res = queryset.paginate(page=int(front_dt_start)//int(front_dt_length)+1, per_page=int(front_dt_length))
    res = queryset.skip(int(front_dt_start)).limit(int(front_dt_length))
    # for r in res.items:
    for r in res:
        # back_dt_data.append([
        #     "", r.content_abbr.status, r.log_time, r.handle_flag,
        #     r.content_abbr.page_size, r.content_abbr.page_no,
        #     r.result.total_count,
        #     r.content_abbr.start_time, r.content_abbr.end_time,
        #     r.result.message, r.result.code
        # ])
        back_dt_data.append({
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
                                "goods_amount": t.goods_amount,
                                "receiver_name": t.receiver_name
                           } for t in r.result.trades]
            })
    back_dt["data"] = back_dt_data
    # 可选。你可以定义一个错误来描述服务器出了问题后的友好提示。
    # back_dt["error"] = ""
    # 自动绑定Id到tr节点上。string。
    # DT_RowId
    # 自动把这个类名添加到 tr。string。
    # DT_RowClass
    # 使用 jQuery.data() 方法把数据绑定到row中，方便之后用来检索（比如加入一个点击事件）。object。
    # DT_RowData
    # 自动绑定数据到 tr上，使用 jQuery.attr() 方法，对象的键用作属性，值用作属性的值。注意这个 需要 Datatables 1.10.5+的版本才支持。object。
    # DT_RowAttr

    # jsonify的作用实际上就是将传入的json形式数据序列化成为json字符串，作为响应的body，并且设置响应的Content-Type为application/json，构造出响应返回至客户端。
    # 直接返回json.dumps的结果是可行的，因为flask会判断并使用make_response方法自动构造出响应，只不过响应头各个字段是默认的。
    # 若要自定义响应字段，则可以使用make_response或Response自行构造响应。
    return jsonify(back_dt)