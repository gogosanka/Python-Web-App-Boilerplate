from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, TextField, BooleanField, SelectField
from wtforms.validators import Required, Length, Email, EqualTo
from datetime import datetime
from smh.models.models import User

class LoginForm(Form):
    nickname = StringField('Username', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class SignupForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required()])
    confirm = PasswordField('Password', validators=[Required(), EqualTo('password', message='Passwords do not match!')])
    nickname = StringField('Username', validators=[Required(), Length(1, 16)]) #confirm if making name longer than 16 handles properly
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Sign Up')

followed = User.query.all()
class VibeMeForm(Form):
    message = StringField('Vibe', validators=[Required(), Length(1, 77)])
    recipient = TextField('Send to:', validators=[Required()])
    submit = SubmitField('Send')

class VibeBroadcast(Form):
    vibe = StringField('Vibe', validators=[Required(), Length(1, 77)])
    followed_list = SelectField('Send to:', choices=[(f,f) for f in followed], validators=[Required()])
    submit = SubmitField('Send')

class UserInformation(Form):
    first_name = TextField('First Name', validators=[Required(), Length(1, 77)])
    last_name = TextField('First Name', validators=[Required(), Length(1, 77)])
    mobile_number = TextField('First Name', validators=[Required(), Length(1, 77)])
    age = TextField('First Name', validators=[Required(), Length(1, 77)])
    city = TextField('First Name', validators=[Required(), Length(1, 77)])
    state = TextField('First Name', validators=[Required(), Length(1, 77)])
    submit = SubmitField('Send')