from wtforms import Form,StringField,PasswordField,validators,TextAreaField,DateTimeField,BooleanField
from wtforms.validators import Required,DataRequired
from wtforms.fields.html5 import DateField

class ArticleForm(Form):
    title = StringField("Başlık",validators=[validators.length(min=1,max=100)])
    content = TextAreaField("Yazı",validators=[validators.length(min=10)])

class RegisterForm(Form):
    username = StringField("Username",validators = [validators.length(min=1,max=30)])
    email = StringField("Email",validators = [validators.Email(message = "Enter a valid email")])
    birthdate = DateField("Birthdate", validators=[Required()])
    password = PasswordField("Password",validators=[validators.DataRequired(message = "Please determine a password"),validators.EqualTo(fieldname="confirm",message="Password is not fit")])
    confirm = PasswordField("Confirm Password")

class LoginForm(Form):
    username = StringField("Username")
    password = PasswordField("Password")
                    