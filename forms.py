from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired


class CreateUser(FlaskForm):
    """Form for creating/registering a user"""

    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])
    email = StringField("email", validators=[InputRequired()])
    first_name = StringField("first name", validators=[InputRequired()])
    last_name = StringField("last name", validators=[InputRequired()])


class LoginUser(FlaskForm):
    """Form for logging in user"""

    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    """Form for adding a feedback"""

    title = StringField("title", validators=[InputRequired()])
    content = StringField("content", validators=[InputRequired()])
