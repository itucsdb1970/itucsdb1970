# -*- coding: utf-8 -*-
"""

@author: Batuhan Özdöl 150180701
"""
#####################################################################
### Assignment skeleton
### You can alter the below code to make your own dynamic website.
### The landing page for assignment 3 should be at /
#####################################################################


from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
import psycopg2 as dbapi2
from forms import *
from passlib.hash import sha256_crypt
from functools import wraps
import os 
import sys
from dbinit import initialize

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
app.config["SECRET_KEY"]="5e30279298f59aff1a8edcc00d1c82d82751b372c2d82f760d194694419211ea"
dsn = "dbname='postgres' user='postgres' host='localhost' password='docker'"


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/dashboard")
@login_required
def dashboard():
    if session["username"]=="admin":
        cursor = mysql.connection.cursor()
        sorgu = "Select * from articles"
        result = cursor.execute(sorgu,)
        if result > 0:
            articles = cursor.fetchall()
            return render_template("dashboard.html",articles=articles)
        else: 
            return render_template("dashboard.html") 
    else:
        cursor = mysql.connection.cursor()
        sorgu = "Select * from articles where author = %s"
        result = cursor.execute(sorgu,(session["username"],))
        if result > 0:
            articles = cursor.fetchall()
            return render_template("dashboard.html",articles=articles)
        else: 
            return render_template("dashboard.html")    

    
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

@app.route("/login",methods=["GET","POST"])    
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data
        cursor = dbapi2.connect(dsn).cursor()
        sorgu = "Select * from USERS where username = %s"
        result = cursor.execute(sorgu,(username,))
        if (result > 0):       # user found
            data = cursor.fetchone() # all infos are taken
            real_password = data["password"]
            cursor.close()
            if(sha256_crypt.verify(password_entered,real_password)): # password matched 
                flash("Giriş başarılı","success")
                session["logged_in"] = True
                session["username"]= username
                if (session["username"]== "admin"):
                    return redirect(url_for("dashboard"))
                return redirect(url_for("articles"))
            else:
                flash("Wrong password","danger")
                return redirect(url_for("login"))
        else:
            cursor.close()
            flash("User not exists","danger")
            return redirect(url_for("login"))
    elif request.method == "GET":
        return render_template("login.html",form=form)
    return render_template("login.html",form=form)    

@app.route("/register",methods=["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate() :   # form validate ise doğru
        username = form.username.data
        cursor = dbapi2.connect(dsn).cursor()
        query = "Select * from USERS where username = %s"
        result = cursor.execute(query,(username,))
        if (result <= 0):           # user not found
            email = form.email.data
            birthDate = form.birthdate.data
            password = sha256_crypt.encrypt(form.password.data)   
            query = "Insert into USERS(username,birthDate,email,password) VALUES (%s,%s,%s,%s)"
            cursor.execute(query,(username,birthDate,email,password)) #tek elemanlıysa (name,)
            mysql.connection.commit()
            cursor.close()
            flash("Registered successfully","success") #message,category
            return redirect(url_for("login"))   
        else:
            cursor.close()
            flash("Username exists !","warning")
            return render_template("register.html",form = form)
    elif request.method == "GET":   
            return render_template("register.html",form = form)
    else: 
            flash("Registration failed","warning")
            return render_template("register.html",form = form)

@app.route("/")
def index():
    return render_template("index.html")

def detail(id):
    return "Article Id:"+id

if __name__ == "__main__":
    app.run(debug=True)



