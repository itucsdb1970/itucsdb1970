import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    "CREATE TABLE IF NOT EXISTS USERS ( id Serial, name varchar(20), surname varchar(20), username varchar(30) NOT NULL UNIQUE, birthDate Date, email Text, password Text NOT NULL, PRIMARY KEY (id))",
    "CREATE TABLE IF NOT EXISTS ARTICLES ( id Serial, title varchar(100) NOT NULL UNIQUE, content Text NOT NULL UNIQUE, type Integer NOT NULL, publishedDate timestamp, PRIMARY KEY (id), FOREIGN KEY (type) REFERENCES TYPES(id) ON DELETE CASCADE ON UPDATE CASCADE)",
    "CREATE TABLE IF NOT EXISTS FAVOURITES ( userid Integer, articleid Integer, PRIMARY KEY(userid, articleid), FOREIGN KEY(userid) REFERENCES USERS(id) ON DELETE CASCADE ON UPDATE CASCADE, FOREIGN KEY(articleid) REFERENCES ARTICLES(id)) ON DELETE CASCADE ON UPDATE CASCADE",
    "INSERT INTO USERS (username,password) VALUES('admin','8C6976E5B5410415BDE908BD4DEE15DFB167A9C873FC4BB8A81F6F2AB448A918')",
]

#"CREATE TABLE IF NOT EXISTS TYPES ( id Serial, type varchar(15) NOT NULL UNIQUE, PRIMARY KEY (id))",

def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()

if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
