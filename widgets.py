#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://richard.to/programming/project-wonderchicken-part-2.html
from html import escape
from wtforms import widgets
from wtforms.compat import text_type
from wtforms.widgets import html_params, Select, HTMLString
from wtforms.fields import Field, SelectField


class SelectOptGroup(object):
    def __init__(self, multiple=False):
        self.multiple = multiple

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        if self.multiple:
            kwargs["multiple"] = True
        html = ["<select %s>" % html_params(name=field.name, **kwargs)]
        for val, label, selected in field.iter_choices():
            if callable(val):
                html.append("<optgroup label='%s'>" % escape(text_type(label)))
                for child_val, child_label, child_selected in val():
                    html.append(Select.render_option(child_val, child_label, child_selected))
                html.append("</optgroup>")
            else:
                html.append(Select.render_option(val, label, selected))
        html.append("</select>")
        return HTMLString("".join(html))


def iter_group(values, data, coerce):
    for value, label in values:
        selected = data is not None and coerce(value) in data
        yield (value, label, selected)


class SelectOptGroupField(Field):
    widget = SelectOptGroup(multiple=True)

    def __init__(self, label=None, validators=None, coerce=text_type, choices=None, **kwargs):
        super(SelectOptGroupField, self).__init__(label, validators, **kwargs)
        self.coerce = coerce
        self.choices = choices

    def iter_choices(self):
        for value, label in self.choices:
            if type(value) is not tuple:
                selected = self.data is not None and self.coerce(value) in self.data
                yield (value, label, selected)
            else:
                selected = False
                yield (lambda: iter_group(value, self.data, self.coerce), label, selected)

    def process_data(self, value):
        try:
            self.data = list(self.coerce(v) for v in value)
        except (ValueError, TypeError):
            self.data = None

    def process_formdata(self, valuelist):
        try:
            self.data = list(self.coerce(x) for x in valuelist)
        except ValueError:
            raise ValueError(self.gettext("Invalid choice(s): one or more data inputs could not be coerced"))

    def pre_validate(self, form):
        values = []
        if self.data:
            for v, _ in self.choices:
                value = v
                if type(v) is tuple:
                    values.extend([cv for cv, _ in v])
                values.append(v)
            for d in self.data:
                if d not in values:
                    raise ValueError(self.gettext("'%(value)s' is not a valid choice for this field") % dict(value=d))


class DivListWidget(object):
    def __init__(self, html_tag='div', prefix_label=True):
        assert html_tag in ('div', 'ol', 'ul')
        self.html_tag = html_tag
        self.prefix_label = prefix_label

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = ['<%s %s>' % (self.html_tag, html_params(**kwargs))]
        for subfield in field:
            if self.prefix_label:
                html.append('<div class="radio clip-radio radio-primary radio-inline">%s %s</div>' % (subfield.label, subfield()))
            else:
                html.append('<div class="radio clip-radio radio-primary radio-inline">%s %s</div>' % (subfield(), subfield.label))
        html.append('</%s>' % self.html_tag)
        return HTMLString(''.join(html))


class InlineRadioField(SelectField):
    """
    Like a SelectField, except displays a list of radio buttons.

    Iterating the field will produce subfields (each containing a label as
    well) in order to allow custom rendering of the individual radio fields.
    """
    widget = DivListWidget(prefix_label=False)
    option_widget = widgets.RadioInput()
