# -*- coding: utf-8 -*-
from flask_wtf import Form
import wtforms


class TaggingForm(Form):
    tags_field = wtforms.SelectMultipleField(label='Tags')
