from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Length, Email, EqualTo
from datetime import datetime

class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class SignupForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    confirm = PasswordField('Password')
    password = PasswordField('Password', validators=[Required(), EqualTo('confirm', message='Passwords must match!')])
    nickname = StringField('Username', validators=[Required(), Length(1, 64)])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Sign Up')
