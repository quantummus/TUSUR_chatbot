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

    # for user in m_users:
    for i in range(0, n[0] - 1):
        # try:
        cursorUsr.execute("SELECT group_name "
                            "FROM users "
                            "WHERE subscribe = 'yes'"
                            "AND user_id = ?", (users_count[i][0], ))
        users_group_name = cursorUsr.fetchone()
        cursorTim.execute("""SELECT timetable.schedule
                                    FROM timetable, users 
                                    WHERE users.user_id = ? 
                                    AND users.group_name=timetable.group_name 
                                    AND 'tomorrow'=date_id""", (users_count[i][0], ))
        m_timetable = cursorTim.fetchone()
        text_group = users_group_name[0]
        text_time = m_timetable[0]
        await bot.api.messages.send(
            user_id=users_count[i][0],
            message=f"Расписание на завтра:({text_group})\n {text_time}",
            random_id=randint(0, 9999999999)
        )
        print("\n\nusers = ", users_count[i][0])
        print("group = ", text_group)
        print("time = ", text_time)
        # except VKAPIError(901):
        #     pass


if __name__ == '__main__':
    asyncio.run(mailing())
