import sqlite3
from sqlite3 import Error
from random import randint


# соединение с БД
def sql_connection():
    try:
        conn = sqlite3.connect('bot.db')
        return conn
    except Error:
        print(Error)


# функция для создания БД
def create_table():
    users = sql_connection()
    cursorUsr = users.cursor()
    cursorUsr.execute("""CREATE TABLE if not exists users
                        (user_id integer PRIMARY KEY, group_name text, subscribe text)
                        """)
    users.commit()

    timetable = sql_connection()
    cursorTim = timetable.cursor()
    cursorTim.execute("""CREATE TABLE if not exists timetable
                        (time_id integer PRIMARY KEY, group_name text, schedule text, date_id text)
                        """)
    # тут вставка расписания с парсинга(?), пока вставила рандомные значения
    data = [(1, '420-1',
             '8:50-10:25: ТВиМС Лекция - Лугина Н.Э.; 13:15-14:50: Иностранный язык Практика рк 125, рк 125а, рк 127,… Серебрякова О.А.;',
             'today'),
            (2, '420-1',
             '8:50-10:25: ТВиМС Практика рк 338 Лугина Н.Э.; 10:40-12:15 ОПР Практика ф 432а, ф 432б Петкун Т.А.16:45-18:20: ОПД Практика - -;',
             'tomorrow'),
            (3, '420-1', 'thisweek_sch', 'thisweek'), (4, '420-1', 'nextweek_sch', 'nextweek'),
            (5, '420-2',
             '8:50-10:25: ТВиМС Лекция - Лугина Н.Э.; 13:15-14:50: Иностранный язык Практика рк 125, рк 125а, рк 127,… Серебрякова О.А.;',
             'today'),
            (6, '420-2', '16:45-18:20: ОПД Практика - -;', 'tomorrow'), (7, '420-2', 'thisweek_sch', 'thisweek'),
            (8, '420-2', 'nextweek_sch', 'nextweek'),
            (9, '420-3',
             '8:50-10:25: ТВиМС Лекция - Лугина Н.Э.; 13:15-14:50: Иностранный язык Практика рк 125, рк 125а, рк 127,… Серебрякова О.А.;',
             'today'),
            (10, '420-3', '16:45-18:20: ОПД Практика - -;', 'tomorrow'), (11, '420-3', 'thisweek_sch', 'thisweek'),
            (12, '420-3', 'nextweek_sch', 'nextweek'),
            (13, '420-4',
             '8:50-10:25: ТВиМС Лекция - Лугина Н.Э.; 13:15-14:50: Иностранный язык Практика рк 125, рк 125а, рк 127,… Серебрякова О.А.;',
             'today'),
            (14, '420-4', '16:45-18:20: ОПД Практика - -;', 'tomorrow'), (15, '420-4', 'thisweek_sch', 'thisweek'),
            (16, '420-4', 'nextweek_sch', 'nextweek')]
    cursorTim.executemany("INSERT OR IGNORE INTO timetable VALUES(?,?,?,?)", data)
    timetable.commit()


def insert_user(group_name: str, subsc):
    if subsc is None:
        subsc = 'no'
    i = randint(0, 999999999)
    user_info = (i, group_name, subsc)
    cursorUsr.execute("INSERT INTO users VALUES(?,?,?)",
                      user_info)  # вставка пользователя в таблицу(id, group)
    users.commit()


# создание 2 таблиц
users = sql_connection()
timetable = sql_connection()
cursorUsr = users.cursor()
cursorTim = timetable.cursor()
create_table()

grouplist = cursorUsr.execute("""SELECT group_name
                                FROM users """)
print(grouplist.fetchall())
# insert_user('420-1', 'yes')
# insert_user('420-2', None)
# insert_user('420-3', 'yes')
# insert_user('420-4', None)

# cursorUsr.execute("SELECT * FROM users")
# print(cursorUsr.fetchall())
#
# cursorUsr.execute("""SELECT * FROM users WHERE subscribe = 'yes'""")
# print(cursorUsr.fetchall())

# day = 'tomorrow'
# m_group = cursorUsr.execute("SELECT group_name "
#                             "FROM users "
#                             "WHERE subscribe = 'yes'")

# m_users = cursorUsr.execute("SELECT user_id "
#                             "FROM users "
#                             "WHERE subscribe = 'yes'")
# m_timetable = cursorTim.execute("""SELECT users.user_id, timetable.schedule
#                                 FROM timetable, users
#                                 WHERE users.subscribe='yes' AND users.group_name=timetable.group_name AND 'tomorrow'=date_id""")
# for user in m_users:
#     user_id = user
#     print(cursorTim.fetchone())

# print('Our BD:')
# cursorObj.execute("SELECT * FROM users")
# cursorObj.execute("""SELECT id, group_name FROM users WHERE group_name = "420-3" """)
# print(cursorObj.fetchall())

users.close()
timetable.close()
