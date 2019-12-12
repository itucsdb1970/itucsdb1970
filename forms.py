from wtforms import Form,StringField,PasswordField,validators,TextAreaField,DateTimeField,BooleanField
from wtforms.validators import Required,DataRequired
from wtforms.fields.html5 import DateField

class ArticleForm(Form):
    title = StringField("Title",validators=[validators.length(min=1,max=100)])
    content = TextAreaField("Content",validators=[validators.length(min=10)])
    source = StringField("Source URL",validators=[validators.length(max=30)])

class MusicForm(Form):
    name = StringField("Name",validators = [validators.length(min=1,max=20)])
    lyrics = TextAreaField("Content",validators=[validators.length(min=10)])
    author = StringField("Author",validators = [validators.length(min=1,max=20)])
    date = DateField('Published Date',validators=(validators.Optional(),))

class RegisterForm(Form):
    username = StringField("Username",validators = [validators.length(min=1,max=35)])
    birthdate = DateField('Birthdate',validators=(validators.Optional(),))
    email = StringField("E-mail",validators = [validators.Email(message = "Please enter a valid email")])
    password = PasswordField("Password",validators=[validators.DataRequired(message = "Enter a password"),
                            validators.EqualTo(fieldname="confirm",message="Password doesn't match !")])
    confirm = PasswordField("Confirm your password")

class LoginForm(Form):
    username = StringField("Username")
    password = PasswordField("Password")