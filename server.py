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

from flask_login import login_user, LoginManager, logout_user
from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from passlib.hash import sha256_crypt
from functools import wraps
from wtforms import Form,StringField,PasswordField,validators,TextAreaField,DateTimeField,BooleanField
from forms import *
import psycopg2 as dbapi2
import os
import sys
import time
import datetime
from operations import *
from user import *

#Kullanıcı giriş decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if "logged_in" in session:
            return f(*args,**kwargs)
        else:
            flash("Please login","danger")
            return redirect(url_for("login"))
    return decorated_function

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThisisSecret'
login = LoginManager(app)
url = "postgres://postgres:root@localhost:5432/postgres"
app.config.from_object("settings")

@login.user_loader
def load_user(user_id):
    return get_user(user_id)

@app.route("/logout")
def logout():
    session.clear()
    logout_user()
    return redirect(url_for("index"))
    

@app.route("/userdashboard")
@login_required
def userdashboard():
    user = find_username(session["username"])
    articles = find_author_inner(user[0])
    musics = find_favourites(user[0])
    return render_template("userdashboard.html",articles=articles,musics=musics)

    
@app.route("/admindashboard")
@login_required
def admindashboard():
    articles = find_articles()
    musics = find_musics()
    return render_template("admindashboard.html",articles=articles,musics=musics)

@app.route("/updateuser",methods=["GET","POST"])
@login_required
def updateuser():
    if request.method == "GET":
        user = find_username(session["username"])
        if user == None:
            flash("User not exists","danger")
            return redirect(url_for("index"))
        else:         
            form = RegisterForm()
            form.username.data = user[1]
            form.birthdate.data = user[4]
            form.email.data = user[2]
            return render_template("updateuser.html",form=form)
    else:
        form = RegisterForm(request.form)
        username = form.username.data
        birthdate = form.birthdate.data
        email = form.email.data
        password = form.password.data
        confirm = form.confirm.data
        user_control = find_username(username)
        if (user_control == None or user_control[1]==username):
            if (confirm != password) :
                flash("Password not match !","danger")
                return render_template("updateuser.html",form=form)
            password = sha256_crypt.encrypt(form.password.data)  
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                sorgu = "Update USERS Set username=%s,birthdate=%s,email=%s,password=%s where USERS.username = %s"
                cursor.execute(sorgu,(username,birthdate,email,password,username)) #tek elemanlıysa (name,)
                connection.commit()
                cursor.close()
            flash("User Updated Successfully","success")
            return redirect(url_for("userdashboard"))
        flash("Username is taken !","danger")
        return render_template("updateuser.html",form=form)

@app.route("/articles")
def articles():
    articles = find_articles()
    if (articles != None):
        return render_template("articles.html",articles=articles)
    else:
        return render_template("articles.html")

@app.route("/addmusic",methods=["GET","POST"])
def addmusic():
    form = MusicForm(request.form)
    counter = 0
    if request.method == "POST" and form.validate():
        name = form.name.data
        lyrics = form.lyrics.data
        control = insert_articles_control(name,lyrics)
        if (control == None):
            author = form.author.data
            tip1 = request.form.get("musictype1")
            tip2 = request.form.get("musictype2")
            tip3 = request.form.get("musictype3")
            if (tip1 != None ):
                counter += 1
            if (tip2 != None ):
                counter += 1
            if (tip3 != None ):
                counter += 1
            if (counter >= 2):
                flash("Invalid type value","warning")
                return redirect(url_for("addmusic"))
            if (tip1 != None ):
                tip = tip1
            elif (tip2 != None ):
                tip = tip2
            elif (tip3 != None ):
                tip = tip3
            else:
                tip = None
            date = form.date.data    
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()   
                sorgu = "Insert into musics(name,lyrics,author,type,date) VALUES(%s,%s,%s,%s,%s)" 
                cursor.execute(sorgu,(name,lyrics,author,tip,date))
                cursor.close()
            flash("Music Added Successfully","success")
            return redirect(url_for("admindashboard"))
        flash("This name or lyrics is already exists!",danger)
        return render_template("addmusic.html",form=form)
    return render_template("addmusic.html",form=form)

@app.route("/musics")
def musics():
    musics = find_musics()
    if (musics != None):
        articles = musics
        return render_template("musics.html", musics=musics)
    else:
        return render_template("musics.html")

@app.route("/addarticle",methods=["GET","POST"])
def addarticle():
    form = ArticleForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        content = form.content.data
        control = insert_articles_control(title,content)
        if (control == None):     # if there is no article
            source = form.source.data
            tip = request.form.get("type")
            if (tip == None):
                flash("Article must have a type!","danger")
                return render_template("addarticle.html",form=form) 
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            author = find_username(session["username"])     
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()   
                sorgu = "Insert into articles(title,author,content,type,publishedDate,sourceUrl) VALUES(%s,%s,%s,%s,%s,%s)" 
                cursor.execute(sorgu,(title,author[0],content,tip,timestamp,source))
                cursor.close()
            flash("Article Added Successfully","success")
            if session["username"] == "admin":
                return redirect(url_for("admindashboard"))
            return redirect(url_for("userdashboard"))
        flash("This title or content is already exists!","danger")
        return render_template("addarticle.html",form=form)
    return render_template("addarticle.html",form=form)

@app.route("/edit/<string:id>",methods=["GET","POST"])
@login_required
def update(id):
    if request.method == "GET":
        article = find_articles_id(id)
        if article == None:
            flash("Article not exists","danger")
            return redirect(url_for("index"))
        else:         
            form = ArticleForm()
            form.title.data = article[2]
            form.content.data = article[3]
            form.source.data = article[6]
            return render_template("update.html",form=form)
    else:
        form = ArticleForm(request.form)
        title = form.title.data
        content = form.content.data
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            sorgu = "Update articles Set title = %s ,content = %s where articles.id = %s"
            cursor.execute(sorgu,(title,content,id,)) #tek elemanlıysa (name,)
            connection.commit()
            cursor.close()
        flash("Article Updated Successfully","success")
        if session["username"] == "admin":
            return redirect(url_for("admindashboard"))
        return redirect(url_for("userdashboard"))

@app.route("/editmusic/<string:id>",methods=["GET","POST"])
@login_required
def updatemusic(id):
    if request.method == "GET":
        music = find_musics_id(id)
        if music == None:
            flash("Article not exists","danger")
            return redirect(url_for("index"))
        else:         
            form = MusicForm()
            form.name.data = music[1]
            form.lyrics.data = music[2]
            form.author.data = music[3]
            return render_template("updatemusic.html",form=form)
    else:
        form = MusicForm(request.form)
        name = form.name.data
        lyrics = form.lyrics.data
        author = form.author.data
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            sorgu = "Update MUSICS Set name = %s ,lyrics = %s,author = %s where musics.id = %s"
            cursor.execute(sorgu,(name,lyrics,author,id,)) #tek elemanlıysa (name,)
            connection.commit()
            cursor.close()
        flash("Music Updated Successfully","success")
        return redirect(url_for("admindashboard"))

@app.route("/fav/<string:id>",methods=["GET","POST"])
@login_required
def fav(id):
    if request.method == "GET":
        music = find_musics_id(id)
        if music == None:
            flash("Article not exists","danger")
            return redirect(url_for("index"))
        else:   
            userid = find_username(session["username"])      
            favourites = find_fav(userid[0],id)
            if (favourites != None):
                flash("This music has already favved","danger")
                return redirect(url_for("musics"))
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                sorgu = "Insert into FAVOURITES(userid,musicid) VALUES (%s,%s)"
                cursor.execute(sorgu,(userid[0],id)) #tek elemanlıysa (name,)
                connection.commit()
                musics = find_favourites(userid[0])
                cursor.close()
            user = find_username(session["username"])
            articles = find_author_inner(user[0])
            flash("Added to favourites","success")
            return render_template("userdashboard.html",musics=musics,articles=articles)

@app.route("/unfav/<string:id>",methods=["GET","POST"])
@login_required
def unfav(id):
    if request.method == "GET":
        music = find_musics_id(id)
        if music == None:
            flash("Article not exists","danger")
            return redirect(url_for("index"))
        else:   
            userid = find_username(session["username"])
            delete_fav(userid[0],id)
            flash("Music Unfavved","success")
            user = find_username(session["username"])
            articles = find_author_inner(user[0])
            musics = find_favourites(user[0])
            return render_template("userdashboard.html",articles=articles,musics=musics)

@app.route("/search",methods=["GET","POST"])
def search():
    if request.method=="GET":
        return redirect(url_for("index"))
    else:
        keyword  = request.form.get("keyword")
        articles = find_keyword(keyword)
        
        if articles == None:
            flash("Nothing found !","warning")
            return redirect(url_for("articles"))
        else:
            return render_template("articles.html",articles=articles)


@app.route("/searchmusic",methods=["GET","POST"])
def searchmusic():
    if request.method=="GET":
        return redirect(url_for("index"))
    else:
        keyword  = request.form.get("keyword")
        musics = find_keyword_music(keyword)
        if musics == None:
            flash("Nothing found !","warning")
            return redirect(url_for("musics"))
        else:
            return render_template("musics.html",musics=musics)

@app.route("/delete/<string:id>")
@login_required
def delete(id):
    result = find_articles_id(id)
    if result != None:
        delete_articles_id(id)
        if session["username"] == "admin":
            redirect(url_for("admindashboard"))
        return redirect(url_for("userdashboard"))
    else:
        flash("Article not exists","danger")
        return redirect(url_for("index"))
            
@app.route("/deletemusic/<string:id>")
@login_required
def deletemusic(id):
    result = find_musics_id(id)
    if result != None:
        delete_musics_id(id)
        flash("Music deleted","success")
        return redirect(url_for("admindashboard"))
    else:
        flash("Music not exists","danger")
        return redirect(url_for("index"))

@app.route("/music/<string:id>")
def music(id):
    music = find_musics_id(id)
    if music != None:
        return render_template("music.html",music=music)
    else:
        return render_template("music.html")

@app.route("/deleteuser")
@login_required
def deleteuser():
    delete_user_username(session["username"])
    session.clear()
    logout_user()
    return redirect(url_for("index"))

@app.route("/article/<string:id>")
def article(id):
    article = find_articles_id(id)
    if article != None:
        return render_template("article.html",article=article)
    else:
        return render_template("article.html")

@app.route("/login",methods=["GET","POST"])    
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data
        result = find_username(username)
        if (result != None):
            data = result #tüm bilgiler alındı         
            real_password = data[5]
            if( sha256_crypt.verify(password_entered,real_password)):   
                if (request.form.get("login")!= None):
                    flash("Login successfully","success")  
                    user = User(data[3],data[2],data[3],data[4],data[5])
                    user.set_id(data[0])
                    login_user(user,remember=True)
                    session["username"] = username
                    session["logged_in"] = True
                    return redirect(url_for("index"))  
                flash("Login successfully","success")
                user = User(data[3],data[2],data[3],data[4],data[5])
                user.set_id(data[0])
                login_user(user,remember=False)
                session["logged_in"] = True
                session["username"]=username
                return redirect(url_for("index"))
            else:
                flash("Wrong password","danger")
                return redirect(url_for("login"))
        else:
            flash("User not exists !","danger")
            return redirect(url_for("login"))
    elif request.method == "GET":
        return render_template("login.html",form=form)
    return render_template("login.html",form=form)

@app.route("/register",methods=["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate() :   # form validate ise doğru
        username = form.username.data
        result = find_username(username)
        if (result == None):
            gender = request.form.get("gender")
            birthdate = form.birthdate.data
            email = form.email.data
            if (birthdate==None and gender==None):
                password = sha256_crypt.encrypt(form.password.data)   
                with dbapi2.connect(url) as connection:
                    cursor = connection.cursor()
                    sorgu = "Insert into users(username,email,password) VALUES (%s,%s,%s)"
                    cursor.execute(sorgu,(username,email,password)) #tek elemanlıysa (name,)
                    connection.commit()
                    cursor.close()
                flash("Registered successfully","success") #message,category
                return redirect(url_for("login"))   
            elif (gender == None):
                password = sha256_crypt.encrypt(form.password.data) 
                with dbapi2.connect(url) as connection:
                    cursor = connection.cursor() 
                    sorgu = "Insert into users(username,email,birthdate,gender,password) VALUES (%s,%s,%s,NULL,%s)"
                    cursor.execute(sorgu,(username,email,birthdate,password)) #tek elemanlıysa (name,)
                    connection.commit()
                    cursor.close()
                flash("Registered successfully","success") #message,category
                return redirect(url_for("login"))   
            elif (birthdate == None):
                password = sha256_crypt.encrypt(form.password.data)  
                with dbapi2.connect(url) as connection:
                    cursor = connection.cursor() 
                    sorgu = "Insert into users(username,email,birthdate,gender,password) VALUES (%s,%s,NULL,%s,%s)"
                    cursor.execute(sorgu,(username,email,gender,password)) #tek elemanlıysa (name,)
                    connection.commit()
                    cursor.close()
                flash("Registered successfully","success") #message,category
                return redirect(url_for("login"))   
            else:
                password = sha256_crypt.encrypt(form.password.data)   
                with dbapi2.connect(url) as connection:
                    cursor = connection.cursor()
                    print(gender)
                    sorgu = "Insert into users(username,email,birthdate,gender,password) VALUES (%s,%s,%s,%s,%s)"
                    cursor.execute(sorgu,(username,email,birthdate,gender,password)) #tek elemanlıysa (name,)
                    connection.commit()
                    cursor.close()
                flash("Registered successfully","success") #message,category
                return redirect(url_for("login"))   
        else:
            flash("Username already exists","warning")
            return render_template("register.html",form = form)
    elif request.method == "GET":   
        return render_template("register.html",form = form)
    else: 
        flash("Unsuccessful operation","warning")
        return render_template("register.html",form = form)

@app.route("/")
def index():
    logout_user()
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
