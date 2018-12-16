from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
  
class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
  
    class Meta:
        csrf = False

class UserCreateForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=1, max=256)])
    username = StringField("Username", [validators.Length(min=1, max=256)])
    password = PasswordField("Password", [validators.Length(min=1, max=256)])
  
    class Meta:
        csrf = False