#!/usr/bin/env python
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, SelectMultipleField, RadioField, ValidationError
from wtforms.validators import DataRequired

from widgets import SelectOptGroupField, InlineRadioField


class ExecPlanQueryForm(FlaskForm):
    qcc_exectime = BooleanField(id="qcc-exectime", default=True)
    qcd_exectime_start = StringField(id="qcd-exectime-start",
                                     validators=[DataRequired()],
                                     default=datetime.utcnow().strftime("%m/%d/%Y"))
    qcd_exectime_end = StringField(id="qcd-exectime-end",
                                   validators=[DataRequired()],
                                   default=datetime.utcnow().strftime("%m/%d/%Y"))
    qcc_biztypes = BooleanField(id="qcc-biztypes", default=False)
    qcd_biztypes = SelectOptGroupField(id="qcd-biztypes",
                                       # render_kw={
                                       #     "disabled": ""
                                       # }
                                       )
    qcd_handled = InlineRadioField(id="qcd-handled")

    def __init__(self, *args, **kwargs):
        super(ExecPlanQueryForm, self).__init__(*args, **kwargs)

        # 查询时间必选。
        self.qcc_exectime.data = True
        # 如果未选择业务类型，多选框禁用。
        if not kwargs.get("qcc_biztypes", True):
            self.qcd_biztypes.render_kw = {"disabled": "disabled"}
        self.qcd_biztypes.choices = [
                                        (
                                            (
                                                ("pull_refunds", "refund"),
                                                ("pull_stock_pds", "inventory"),
                                                ("pull_stock_transfers", "shifting"),
                                                ("pull_stockin_orders", "stockin"),
                                                ("pull_stockout_orders", "stockout"),
                                                ("pull_trades", "trade"),
                                            ),
                                            "Processed"
                                        ),
                                        (
                                            (
                                                ("pull_refunds_finished", "refund_finished"),
                                                ("pull_trades_finished", "trade_finished"),
                                            ),
                                            "Finished"
                                        ),
                                        # ("Value 6", "Label 6"),
                                        # ("Value 7", "Label 7"),
                                       ]
        self.qcd_handled.choices = [("1", "all"),
                                    ("2", "handled"),
                                    ("3", "unhandled")]

    # def _validate_exectime_interval(self):
    #     if self.qcd_exectime_start.data and self.qcd_exectime_end.data:
    #         s = datetime.strptime(self.qcd_exectime_start.data, "%m/%d/%Y")
    #         e = datetime.strptime(self.qcd_exectime_end.data, "%m/%d/%Y")
    #         if (e-s).days > 10:
    #             raise ValidationError("The date interval should not exceed 10 days")
    #
    # def validate_qcd_exectime_start(self, field):
    #     self._validate_exectime_interval()
    #
    # def validate_qcd_exectime_end(self, field):
    #     self._validate_exectime_interval()


class VoucherQueryForm(FlaskForm):
    qcc_logtime = BooleanField(id="qcc-logtime", default=True)
    qcd_logtime_start = StringField(id="qcd-logtime-start",
                                     validators=[DataRequired()],
                                     default=datetime.utcnow().strftime("%m/%d/%Y"))
    qcd_logtime_end = StringField(id="qcd-logtime-end",
                                   validators=[DataRequired()],
                                   default=datetime.utcnow().strftime("%m/%d/%Y"))
    qcd_handled = InlineRadioField(id="qcd-handled")

    def __init__(self, *args, **kwargs):
        super(VoucherQueryForm, self).__init__(*args, **kwargs)

        # 查询时间必选。
        self.qcc_logtime.data = True
        self.qcd_handled.choices = [("1", "all"),
                                    ("2", "handled"),
                                    ("3", "unhandled")]

    # def _validate_logtime_interval(self):
    #     if self.qcd_logtime_start.data and self.qcd_logtime_end.data:
    #         s = datetime.strptime(self.qcd_logtime_start.data, "%m/%d/%Y")
    #         e = datetime.strptime(self.qcd_logtime_end.data, "%m/%d/%Y")
    #         if (e-s).days > 10:
    #             raise ValidationError("The date interval should not exceed 10 days")
    #
    # def validate_qcd_logtime_start(self, field):
    #     self._validate_logtime_interval()
    #
    # def validate_qcd_logtime_end(self, field):
    #     self._validate_logtime_interval()
