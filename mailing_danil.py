import asyncio
from vkbottle import VKAPIError
from vkbottle.bot import Bot

from bd import *

bot = Bot("ba11cc5d4ee4bd92628131613bc774856efcb57c2b89b44295941c51ca249da41c22fd69fae0f61aabd32")

sqlite3.connect('bot.db')

# работает только когда запускаешь код, нужен какой-то таймер или что-то
async def mailing():
    users = sql_connection()
    timetable = sql_connection()
    cursorUsr = users.cursor()
    cursorTim = timetable.cursor()

    m_users = cursorUsr.execute("SELECT user_id "
                                "FROM users "
                                "WHERE subscribe = 'yes'")
    users_count = cursorUsr.fetchall()
    m_users.execute("SELECT Count(*) FROM users")
    n = m_users.fetchone()
    # изменить! сделать эксекют и фетч в цикле?
    group_user = cursorTim.execute("""SELECT timetable.group_name
                                        FROM timetable, users 
                                        WHERE users.subscribe='yes' AND users.group_name=timetable.group_name AND 'tomorrow'=date_id""")
    group_user = cursorTim.fetchall()
    cursorTim.execute("""SELECT timetable.schedule
                            FROM timetable, users 
                            WHERE users.subscribe='yes' AND users.group_name=timetable.group_name AND 'tomorrow'=date_id""")
    m_timetable = cursorTim.fetchall()

    # for user in m_users:
    for i in range(0, n[0] - 1):
        # try:
        text_group = group_user[i][0]
        text_time = m_timetable[i][0]
        # проблема в этом? Я не понимаю как работает эта вещь
        await bot.api.messages.send(
            user_id=users_count[i][0],
            message=f"Расписание на завтра:({text_group})\n {text_time}",
            random_id=randint(0, 9999999999)
        )
        # путает юзеров и их группы? Но высылает то все равно только одну
        print("\n\nusers = ", users_count[i][0])
        print("group = ", text_group)
        print("time = ", text_time)
        # except VKAPIError(901):
        #     pass


if __name__ == '__main__':
    asyncio.run(mailing())
