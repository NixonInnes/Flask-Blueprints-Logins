from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length


class ExampleForm(Form):
    text = StringField('Text: ', default='A default string', validators=[Required(), Length(5)])
    submit = SubmitField()
