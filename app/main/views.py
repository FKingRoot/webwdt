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

    form.qcc_logtime.data = qcc_logtime
    form.qcd_logtime_start.data = start_time
    form.qcd_logtime_end.data = end_time
    form.qcd_handled.data = handled
    return render_template("trade.html",
                           qcc_logtime=qcc_logtime,
                           start_time=start_time,
                           end_time=end_time,
                           handled=handled,
                           form=form,
                           breadcrumb=["home", "trade"])
