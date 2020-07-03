from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class HelloForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1,50)])
    body = TextAreaField('Message', validators=[DataRequired(), Length(1,200)])
    submit = SubmitField('Commit')

class TelnetForm(FlaskForm):
    ip = StringField('IP',validators=[DataRequired()])
    port = StringField('Port', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    inputcommand = StringField('Command')
    submit = SubmitField('Connect')
    submit1 = SubmitField('Command')
    submit2 = SubmitField('Exit')
