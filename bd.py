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


# функция для создания БД, если ее не существовало до этого
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
             '8:50-10:25: ТВиМС Лекция - Лугина Н.Э.;\n\n13:15-14:50: Иностранный язык Практика рк 125, рк 125а, рк 127,… Серебрякова О.А.;',
             'today'),
            (2, '420-1',
             '8:50-10:25: ТВиМС Практика рк 338 Лугина Н.Э.;\n\n10:40-12:15 ОПР Практика ф 432а, ф 432б Петкун Т.А.16:45-18:20: ОПД Практика - -;',
             'tomorrow'),
            (3, '420-1', 'thisweek_sch', 'thisweek'), (4, '420-1', 'nextweek_sch', 'nextweek'),
            (5, '420-2',
             '8:50-10:25: ТВиМС Лекция - Лугина Н.Э.;\n\n13:15-14:50: Иностранный язык Практика рк 125, рк 125а, рк 127,… Серебрякова О.А.;',
             'today'),
            (6, '420-2', '16:45-18:20: ОПД Практика - -;', 'tomorrow'), (7, '420-2', 'thisweek_sch', 'thisweek'),
            (8, '420-2', 'nextweek_sch', 'nextweek'),
            (9, '420-3',
             '8:50-10:25: ТВиМС Лекция - Лугина Н.Э.;\n\n13:15-14:50: Иностранный язык Практика рк 125, рк 125а, рк 127,… Серебрякова О.А.;',
             'today'),
            (10, '420-3', '16:45-18:20: ОПД Практика - -;', 'tomorrow'), (11, '420-3', 'thisweek_sch', 'thisweek'),
            (12, '420-3', 'nextweek_sch', 'nextweek'),
            (13, '420-4',
             '8:50-10:25: ТВиМС Лекция - Лугина Н.Э.;\n\n13:15-14:50: Иностранный язык Практика рк 125, рк 125а, рк 127,… Серебрякова О.А.;',
             'today'),
            (14, '420-4', '16:45-18:20: ОПД Практика - -;', 'tomorrow'), (15, '420-4', 'thisweek_sch', 'thisweek'),
            (16, '420-4', 'nextweek_sch', 'nextweek')]
    cursorTim.executemany("INSERT OR IGNORE INTO timetable VALUES(?,?,?,?)", data)
    timetable.commit()

# функция для вставки пользователя в бд и изменения группы
def insert_user(i, group_name: str, subsc):
    users = sql_connection()
    cursorUsr = users.cursor()
    if subsc is None:
        subsc = 'no'
    user_info = (i[0].id, group_name, subsc)
    cursorUsr.execute("""SELECT * FROM users WHERE user_id = ?""", (i[0].id,))
    select = cursorUsr.fetchone()
    if select == None:
        cursorUsr.execute("INSERT INTO users VALUES(?,?,?)",
                          user_info)  # вставка пользователя в таблицу(id, group)
        users.commit()
    else:
        cursorUsr.execute("UPDATE users SET group_name = ? WHERE user_id =?", (group_name, i[0].id,))
        users.commit()

# функция для удаления пользователя
def delete_user(user_id: int):
    users = sql_connection()
    cursorUsr = users.cursor()
    cursorUsr.execute("""DELETE FROM users WHERE user_id = ?""", (user_id,))
    users.commit()


def delete_all():
    users = sql_connection()
    cursorUsr = users.cursor()
    cursorUsr.execute("""DELETE FROM users""")
    users.commit()


def get_schedule(group: str, date: str):
    timetable = sql_connection()
    cursorTim = timetable.cursor()
    cursorTim.execute("""SELECT schedule FROM timetable WHERE group_name = ? AND date_id =?""", (group[0], date,))
    schedule = cursorTim.fetchone()
    return schedule[0]


def update_schedule():  # функция для обновления расписания(вписывает значения data в бд)
    timetable = sql_connection()
    cursorTim = timetable.cursor()
    cursorTim.execute("""DELETE FROM timetable""")
    data = [(1, '420-1',
             '8:50-10:25: ТВиМС Лекция - Лугина Н.Э.;\n\n13:15-14:50: Иностранный язык Практика рк 125, рк 125а, рк 127,… Серебрякова О.А.;',
             'today'),
            (2, '420-1',
             '8:50-10:25: ТВиМС Практика рк 338 Лугина Н.Э.;\n\n10:40-12:15 ОПР Практика ф 432а, ф 432б Петкун Т.А.16:45-18:20: ОПД Практика - -;',
             'tomorrow'),
            (3, '420-1', 'thisweek_sch', 'thisweek'), (4, '420-1', 'nextweek_sch', 'nextweek'),
            (5, '420-2',
             '8:50-10:25: ТВиМС Лекция - Лугина Н.Э.;\n\n13:15-14:50: Иностранный язык Практика рк 125, рк 125а, рк 127,… Серебрякова О.А.;',
             'today'),
            (6, '420-2', '16:45-18:20: ОПД Практика - -;', 'tomorrow'), (7, '420-2', 'thisweek_sch', 'thisweek'),
            (8, '420-2', 'nextweek_sch', 'nextweek'),
            (9, '420-3',
             '8:50-10:25: ТВиМС Лекция - Лугина Н.Э.;\n\n13:15-14:50: Иностранный язык Практика рк 125, рк 125а, рк 127,… Серебрякова О.А.;',
             'today'),
            (10, '420-3', '16:45-18:20: ОПД Практика - -;', 'tomorrow'), (11, '420-3', 'thisweek_sch', 'thisweek'),
            (12, '420-3', 'nextweek_sch', 'nextweek'),
            (13, '420-4',
             '8:50-10:25: ТВиМС Лекция - Лугина Н.Э.;\n\n13:15-14:50: Иностранный язык Практика рк 125, рк 125а, рк 127,… Серебрякова О.А.;',
             'today'),
            (14, '420-4', '16:45-18:20: ОПД Практика - -;', 'tomorrow'), (15, '420-4', 'thisweek_sch', 'thisweek'),
            (16, '420-4', 'nextweek_sch', 'nextweek')]
    cursorTim.executemany("INSERT INTO timetable VALUES(?,?,?,?)", data)
    timetable.commit()


# создание 2 таблиц
users = sql_connection()
timetable = sql_connection()
cursorUsr = users.cursor()
cursorTim = timetable.cursor()
create_table()

update_schedule()

users.close()
timetable.close()
