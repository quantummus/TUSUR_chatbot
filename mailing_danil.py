import asyncio
from random import randint

from vkbottle.bot import Bot

from bd import *

bot = Bot("ba11cc5d4ee4bd92628131613bc774856efcb57c2b89b44295941c51ca249da41c22fd69fae0f61aabd32")

sqlite3.connect('bot.db')


async def mailing():
    users = sql_connection()
    timetable = sql_connection()
    cursorUsr = users.cursor()
    cursorTim = timetable.cursor()
    m_users = cursorUsr.execute("SELECT user_id "
                                "FROM users "
                                "WHERE subscribe = 'yes'")
    m_timetable = cursorTim.execute("""SELECT timetable.schedule 
                                    FROM timetable, users 
                                    WHERE users.subscribe='yes' AND users.group_name=timetable.group_name AND 'tomorrow'=date_id""")
    for user in m_users:
        try:
            await bot.api.messages.send(
            user_id=user,
            message=f"Расписание: {m_timetable.fetchone()}",
            random_id=randint(0, 9999999999)
        )
        except VKAPIError(901):
            pass


if __name__ == '__main__':
    asyncio.run(mailing())
