import os
import sys

import psycopg2 as dbapi2

INIT_STATEMENTS = [
    "CREATE TABLE IF NOT EXISTS USERS (id Serial, username varchar(20) NOT NULL UNIQUE, email varchar(30) NOT NULL UNIQUE, gender varchar(1),birthDate Date, password Text NOT NULL, PRIMARY KEY (id))",
    "CREATE TABLE IF NOT EXISTS ARTICLES (id Serial, author Integer NOT NULL, title varchar(100) NOT NULL UNIQUE, content Text NOT NULL UNIQUE, type varchar(15) NOT NULL, publishedDate timestamp, sourceUrl varchar(30), PRIMARY KEY (id), FOREIGN KEY(author) REFERENCES USERS(id) ON DELETE CASCADE ON UPDATE CASCADE)",
    "CREATE TABLE IF NOT EXISTS MUSICS (id Serial, name varchar(20) NOT NULL UNIQUE, lyrics Text NOT NULL UNIQUE, author varchar(20) NOT NULL, type varchar(10), date Date, PRIMARY KEY(id))",
    "CREATE TABLE IF NOT EXISTS FAVOURITES (userid Integer, musicid Integer, PRIMARY KEY(userid, musicid), FOREIGN KEY(userid) REFERENCES USERS(id) ON DELETE CASCADE ON UPDATE CASCADE, FOREIGN KEY(musicid) REFERENCES MUSICS(id) ON DELETE CASCADE ON UPDATE CASCADE)",
]

def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()

# for elephant sql url = postgres://ocponcdw:3qJhgtvyyELu7FXS4FSujJEWJGoYx3V9@raja.db.elephantsql.com:5432/ocponcdw

if __name__ == "__main__":
    url = "postgres://postgres:root@localhost:5432/postgres"
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
