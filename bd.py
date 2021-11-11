import sqlite3
from sqlite3 import Error


def sql_connection():
    try:
        conn = sqlite3.connect('bot.db')
        return conn
    except Error:
        print(Error)


def create_table():
    conn = sql_connection()
    cursorObj = conn.cursor()
    cursorObj.execute("""CREATE TABLE if not exists users
                        (id integer PRIMARY KEY, surname text, name text, f_name text, group_name text)
                        """)
    conn.commit()

conn = sql_connection()
create_table()
cursorObj = conn.cursor()
cursorObj.execute("INSERT INTO users VALUES (1,'Ivanova','Natalya' ,'Sergeevna','420-4')")
cursorObj.execute("INSERT INTO users VALUES (2,'Yakovleva','Natalya' ,'Sergeevna','420-3')")
cursorObj.execute("INSERT INTO users VALUES (3,'Yakovleva','Natalya' ,'Sergeevna','420-2')")
cursorObj.execute("INSERT INTO users VALUES (4,'Kovleva','Natalya' ,'Sergeevna','420-3')")
cursorObj.execute("INSERT INTO users VALUES (5,'Yakovleva','Natalya' ,'Sergeevna','420-3')")
conn.commit()

print('Our BD:')
cursorObj.execute("SELECT * FROM users")
cursorObj.execute("""SELECT id, group_name FROM users WHERE group_name = "420-3" """)
print(cursorObj.fetchall())
