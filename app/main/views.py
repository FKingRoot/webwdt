#!/usr/bin/env python
from datetime import datetime
from flask import (current_app, url_for, request, session, render_template, redirect, make_response, abort, g)
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries

from . import main
from .forms import ExecPlanQueryForm
from app import db
from app.models.user import Role, User
from app.models.mongo_model import ExecutionPlan

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

    pagination = ExecutionPlan.objects(type__in=biz_types) \
        .order_by("-exec_time", "type") \
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
                           form=form,
                           breadcrumb=["home", "execplan"],
                           exec_plans=exec_plans)
