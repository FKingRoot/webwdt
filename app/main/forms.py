from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired


class ExecPlanQueryForm(FlaskForm):
    qcc_exectime = BooleanField(id="qcc-exectime",
                                render_kw={"checked": ""})
    qcd_exectime_start = StringField(id="qcd-exectime-start",
                                     render_kw={
                                         "value": datetime.utcnow().strftime("%m/%d/%Y"),
                                         # "disabled": ""
                                     })
    qcd_exectime_end = StringField(id="qcd-exectime-end",
                                   render_kw={
                                       "value": datetime.utcnow().strftime("%m/%d/%Y"),
                                       # "disabled": ""
                                   })
    qcc_biztypes = BooleanField(id="qcc-biztypes")
    qcd_biztypes = SelectMultipleField(id="qcd-biztypes", choices=[])
    qcc_handled = BooleanField(id="qcc-handled")
    qcd_handled = BooleanField(id="qcd-handled")
