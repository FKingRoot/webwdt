#!/usr/bin/env python
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, SelectMultipleField, ValidationError
from wtforms.validators import DataRequired

from widgets import SelectOptGroupField


class ExecPlanQueryForm(FlaskForm):
    qcc_exectime = BooleanField(id="qcc-exectime",
                                render_kw={"checked": ""})
    qcd_exectime_start = StringField(id="qcd-exectime-start",
                                     validators=[DataRequired()],
                                     render_kw={
                                         "value": datetime.utcnow().strftime("%m/%d/%Y"),
                                     })
    qcd_exectime_end = StringField(id="qcd-exectime-end",
                                   validators=[DataRequired()],
                                   render_kw={
                                       "value": datetime.utcnow().strftime("%m/%d/%Y"),
                                   })
    qcc_biztypes = BooleanField(id="qcc-biztypes")
    qcd_biztypes = SelectOptGroupField(id="qcd-biztypes",
                                       render_kw={
                                           "disabled": ""
                                       })
    qcc_handled = BooleanField(id="qcc-handled")
    qcd_handled = BooleanField(id="qcd-handled",
                               render_kw={
                                   "disabled": ""
                               })

    def __init__(self, *args, **kwargs):
        super(ExecPlanQueryForm, self).__init__(*args, **kwargs)
        self.qcd_biztypes.choices = [
                                        (
                                            (
                                                ("PRF", "refund"),
                                                ("PIV", "inventory"),
                                                ("PSF", "shifting"),
                                                ("PSI", "stockin"),
                                                ("PSO", "stockout"),
                                                ("PTR", "trade"),
                                            ),
                                            "Processed"
                                        ),
                                        (
                                            (
                                                ("FRF", "refund_finished"),
                                                ("FTR", "trade_finished"),
                                            ),
                                            "Finished"
                                        ),
                                        # ("Value 6", "Label 6"),
                                        # ("Value 7", "Label 7"),
                                       ]

    def _validate_exectime_interval(self):
        if self.qcd_exectime_start.data and self.qcd_exectime_end.data:
            s = datetime.strptime(self.qcd_exectime_start.data, "%m/%d/%Y")
            e = datetime.strptime(self.qcd_exectime_end.data, "%m/%d/%Y")
            if (e-s).days > 10:
                raise ValidationError("The date interval should not exceed 10 days")

    def validate_qcd_exectime_start(self, field):
        self._validate_exectime_interval()

    def validate_qcd_exectime_end(self, field):
        self._validate_exectime_interval()
