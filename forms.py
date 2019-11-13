from wtforms import Form,StringField,PasswordField,validators,TextAreaField,DateTimeField,BooleanField
from wtforms.validators import Required,DataRequired
from wtforms.fields.html5 import DateField

class ArticleForm(Form):
    title = StringField("Başlık",validators=[validators.length(min=1,max=100)])
    content = TextAreaField("Yazı",validators=[validators.length(min=10)])

class RegisterForm(Form):
    name = StringField("Ad",validators = [validators.length(min=1,max=20)])
    surname = StringField("Soyad",validators = [validators.length(min=1,max=20)])
    username = StringField("Kullanıcı Adı",validators = [validators.length(min=1,max=35)])
    birthdate = DateField('Birthdate',validators=(validators.Optional(),))
    email = StringField("Email",validators = [validators.Email(message = "Lütfen geçerli email giriniz")])
    password = PasswordField("Parola:",validators=[validators.DataRequired(message = "Lütfen parola belirleyiniz"),validators.EqualTo(fieldname="confirm",message="Parolanız uyuşmuyor.")])
    confirm = PasswordField("Parola Doğrula")

class LoginForm(Form):
    username = StringField("Username")
    password = PasswordField("Password")
                    