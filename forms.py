from flask_wtf import FlaskForm
from wtforms import StringField, Floatfield, IntegerField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Email, Optional

class CreateUser(FlaskForm):
    """Form for creating/registering a user"""
    
    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])

class LoginUser(FlaskForm):
    """Form for logging in user"""
    
    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])