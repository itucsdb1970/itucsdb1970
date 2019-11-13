# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 17:37:11 2019

@author: Batuhan
"""
#####################################################################
### Assignment skeleton
### You can alter the below code to make your own dynamic website.
### The landing page for assignment 3 should be at /
#####################################################################


from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,PasswordField,validators,TextAreaField
from passlib.hash import sha256_crypt
from functools import wraps
from forms import *

#Kullanıcı giriş decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if "logged_in" in session:
            return f(*args,**kwargs)
        else:
            flash("Lütfen giriş yapın","danger")
            return redirect(url_for("login"))
    return decorated_function


app = Flask(__name__)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
    
@app.route("/userdashboard")
@login_required
def userdashboard():
    cursor = mysql.connection.cursor()
    sorgu = "Select * from articles where author = %s"
    result = cursor.execute(sorgu,(session["username"],))
    if result > 0:
        articles = cursor.fetchall()
        return render_template("user-dashboard.html",articles=articles)
    else: 
        return render_template("user-dashboard.html")
    
@app.route("/admindashboard")
@login_required
def admindashboard():
    cursor = mysql.connection.cursor()
    sorgu = "Select * from articles"
    result = cursor.execute(sorgu,)
    if result > 0:
        articles = cursor.fetchall()
        return render_template("admin-dashboard.html",articles=articles)
    else: 
        return render_template("admin-dashboard.html")

@app.route("/login",methods=["GET","POST"])    
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data
        cursor = mysql.connection.cursor()
        sorgu = "Select * from users where username = %s"
        result = cursor.execute(sorgu,(username,))
        if (result > 0 ):
            data = cursor.fetchone() #tüm bilgiler alındı
            real_password = data["password"]
            if( sha256_crypt.verify(password_entered,real_password)):   
                """if (request.form.get("login")!= None):
                    flash("Giriş başarılı","success")  
                    user = User(data["username"],data["email"],data["birthdate"],data["password"],data["gender"])
                    user.set_id(data["id"])
                    login_user(user,remember=True)
                    session["logged_in"] = True
                    session["username"]= username
                    return redirect(url_for("index")) """    
                flash("Giriş başarılı","success")
                session["logged_in"] = True
                session["username"]= username
                return redirect(url_for("index"))
            else:
                flash("Parola yanlış","danger")
                return redirect(url_for("login"))
        else:
            flash("Kullanıcı bulunmuyor","danger")
            return redirect(url_for("login"))
    elif request.method == "GET":
        return render_template("login.html",form=form)
    return render_template("login.html",form=form)

@app.route("/articles")
def articles():
    cursor = mysql.connection.cursor()
    sorgu = "Select * from articles"
    result = cursor.execute(sorgu)
    if ( result > 0 ):
        articles = cursor.fetchall()
        return render_template("articles.html",articles=articles)
    else:
        return render_template("articles.html")
    
@app.route("/addarticle",methods=["GET","POST"])
def addarticle():
    form = ArticleForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        content = form.content.data
        cursor = mysql.connection.cursor()
        sorgu = "Insert into articles(title,author,content) VALUES(%s,%s,%s)" 
        cursor.execute(sorgu,(title,session["username"],content))
        mysql.connection.commit()
        cursor.close()
        flash("Yazınız eklendi","success")
        return redirect(url_for("dashboard"))
    return render_template("addarticle.html",form=form)

@app.route("/edit/<string:id>")
@login_required
def update(id):
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        sorgu = "Select * from articles where id = %s and author = %s"
        result = cursor.execute(sorgu,(id,session["username"]))
        if result ==0:
            flash("Yetki yok","danger")
            return redirect(url_for("index"))
        else:
            article = cursor.fetchone()           
            form = ArticleForm()
            form.title.data = article["title"]
            form.content.data = article["content"]
            return render_template("update.html",form=form)
    else:
        form = ArticleForm(request.form)
        title = form.title.data
        content = form.content.data
        sorgu2 = "Update articles Set title = %s and content = %s where id = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(sorgu2,(title,content,id))
        mysql.connection.commit()
        flash("Yazınız güncellendi","success")
        return redirect(url_for("dashboard"))
        
@app.route("/search",methods=["GET","POST"])
def search():
    if request.method=="GET":
        return redirect(url_for("index"))
    else:
        keyword  = request.form.get("keyword")
        cursor = mysql.connection.cursor()
        sorgu = "Select * from articles where title like '%" + keyword + "%'"
        result = cursor.execute(sorgu)
        
        if result==0:
            flash("Yazı bulunamadı","warning")
            return redirect(url_for("articles"))
        else:
            articles = cursor.fetchall()
            return render_template("articles.html",articles=articles)

@app.route("/delete/<string:id>")
#@login_required
def delete(id):
    cursor = mysql.connection.cursor()
    sorgu = "Select * from articles where author = %s and id=%s"
    result = cursor.execute(sorgu,(session["username"],id))
    if result>0:
        sorgu2 = "Delete from articles id=%s"
        cursor.execute(sorgu2,(id,))
        mysql.connection.commit()
        return redirect(url_for("dashboard"))
    else:
        flash("Yetki yok","danger")
        return redirect(url_for("index"))
            
    
    
@app.route("/article/<string:id>")
def article(id):
    cursor = mysql.connection.cursor()
    sorgu = "Select * from articles where id = %s"
    result = cursor.execute(sorgu,(id,))
    if result>0:
        article = cursor.fetchone()
        return render_template("article.html",article=article)
    else:
        return render_template("article.html")

@app.route("/register",methods=["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate() :   # form validate ise doğru
        name = form.name.data
        surname = form.surname.data
        username = form.username.data
        cursor = mysql.connection.cursor()
        sorgu2 = "Select * from users where username = %s"
        result = cursor.execute(sorgu2,(username,))    
        if (result <= 0):
            gender = request.form.get("gender")
            birthdate = form.birthdate.data
            email = form.email.data
            if (birthdate==None and gender==None):
                password = sha256_crypt.encrypt(form.password.data)   
                sorgu = "Insert into users(name,surname,username,email,password) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(sorgu,(name,surname,username,email,password)) #tek elemanlıysa (name,)
                mysql.connection.commit()
                cursor.close()
                flash("Başarılı","success") #message,category
                return redirect(url_for("login"))   
            elif (gender == None):
                password = sha256_crypt.encrypt(form.password.data)   
                sorgu = "Insert into users(name,surname,username,email,birthdate,gender,password) VALUES (%s,%s,%s,%s,%s,NULL,%s)"
                cursor.execute(sorgu,(name,surname,username,email,birthdate,password)) #tek elemanlıysa (name,)
                mysql.connection.commit()
                cursor.close()
                flash("Başarılı","success") #message,category
                return redirect(url_for("login"))   
            elif (birthdate == None):
                password = sha256_crypt.encrypt(form.password.data)   
                sorgu = "Insert into users(name,surname,username,email,birthdate,gender,password) VALUES (name,surname,%s,%s,NULL,%s,%s)"
                cursor.execute(sorgu,(name,surname,username,email,str(gender),password)) #tek elemanlıysa (name,)
                mysql.connection.commit()
                cursor.close()
                flash("Başarılı","success") #message,category
                return redirect(url_for("login"))   
            else:
                password = sha256_crypt.encrypt(form.password.data)   
                sorgu = "Insert into users(name,surname,username,email,birthdate,gender,password) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sorgu,(name,surname,username,email,birthdate,str(gender),password)) #tek elemanlıysa (name,)
                mysql.connection.commit()
                cursor.close()
                flash("Başarılı","success") #message,category
                return redirect(url_for("login"))   
        else:
            flash("Kullanıcı adını değiştiriniz.","warning")
            return render_template("register.html",form = form)
    elif request.method == "GET":   
        return render_template("register.html",form = form)
    else: 
        flash("Başarısız","warning")
        return render_template("register.html",form = form)

@app.route("/")
def index():
    return render_template("index.html")

def detail(id):
    return "Article Id:"+id

if __name__ == "__main__":
    app.run(debug=True)
