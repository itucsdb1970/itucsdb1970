import psycopg2 as dbapi2

url = "postgres://ocponcdw:3qJhgtvyyELu7FXS4FSujJEWJGoYx3V9@raja.db.elephantsql.com:5432/ocponcdw"

def find_author_inner(author):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "SELECT * FROM ARTICLES inner join USERS on author = USERS.id  WHERE author = %s"
        cursor.execute(sorgu,(author,))
        user = cursor.fetchall()
        cursor.close()
        return user

def find_author(author):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "SELECT * FROM ARTICLES WHERE author = %s"
        cursor.execute(sorgu,(author,))
        user = cursor.fetchall()
        cursor.close()
        return user

def find_articles():
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "SELECT * FROM ARTICLES"
        cursor.execute(sorgu)
        musics = cursor.fetchall()
        cursor.close()
        return musics

def find_favourites(userid):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "SELECT * FROM FAVOURITES inner join MUSICS on musics.id = musicid  WHERE userid = %s"
        cursor.execute(sorgu,(userid,))
        musics = cursor.fetchall()
        cursor.close()
        return musics

def find_musics_id(id):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "SELECT * FROM MUSICS where id = %s"
        cursor.execute(sorgu,(id,))
        music = cursor.fetchone()
        cursor.close()
        return music

def find_articles_id(id):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "SELECT * FROM ARTICLES where id = %s"
        cursor.execute(sorgu,(id,))
        articles = cursor.fetchone()
        cursor.close()
        return articles

def delete_musics_id(id):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "delete FROM MUSICS where id = %s"
        cursor.execute(sorgu,(id,))
        cursor.close()

def delete_articles_id(id):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "delete FROM ARTICLES where id = %s"
        cursor.execute(sorgu,(id,))
        cursor.close()

def delete_user_username(username):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "delete FROM USERS where username = %s"
        cursor.execute(sorgu,(username,))
        cursor.close()

def find_fav(userid,musicid):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "select * from FAVOURITES where userid= %s and musicid= %s"
        cursor.execute(sorgu,(userid,musicid))
        favs = cursor.fetchone()
        cursor.close()
        return favs
        
def delete_fav(userid,musicid):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "delete FROM FAVOURITES where userid= %s and musicid= %s"
        cursor.execute(sorgu,(userid,musicid))
        cursor.close()

def find_musics():
    with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            sorgu = "SELECT * FROM MUSICS"
            cursor.execute(sorgu)
            musics = cursor.fetchall()
            cursor.close()
            return musics

def insert_musics_control(name,lyrics):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()   
        sorgu = "Select * from musics where name = %s or lyrics = %s" 
        cursor.execute(sorgu,(title,content))
        musics = cursor.fetchall()
        cursor.close()
        return musics   

def insert_articles_control(title,content):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()   
        sorgu = "Select * from articles where title = %s or content = %s" 
        cursor.execute(sorgu,(title,content))
        articles = cursor.fetchone()
        cursor.close()
        return articles

def find_username(username):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "SELECT * FROM USERS WHERE username = %s"
        cursor.execute(sorgu,(username,))
        user = cursor.fetchone()
        cursor.close()
        return user

def find_keyword(keyword):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "Select * from articles where title like '%" + keyword + "%'"
        cursor.execute(sorgu) 
        word = cursor.fetchall()
        connection.commit()
        cursor.close()
        return word

def find_keyword_music(keyword):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        sorgu = "Select * from musics where name like '%" + keyword + "%'"
        cursor.execute(sorgu) 
        word = cursor.fetchall()
        connection.commit()
        cursor.close()
        return word