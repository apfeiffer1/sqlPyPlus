from flask.ext.wtf import Form
from wtforms import widgets, StringField, SelectMultipleField, SubmitField, IntegerField

from wtforms.validators import InputRequired, Optional, Length, Email, Regexp, NumberRange

class InputDB(Form):

    dbUrl = StringField('DB URL')
    submit = SubmitField('Inspect')
