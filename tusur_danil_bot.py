from random import randint

from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, EMPTY_KEYBOARD, VKAPIError

from bd import *

# ------------это не надо трогать---------------

bot = Bot("ba11cc5d4ee4bd92628131613bc774856efcb57c2b89b44295941c51ca249da41c22fd69fae0f61aabd32")
bot.labeler.vbml_ignore_case = True

# ------------это не надо трогать---------------

# подключение к бд
sqlite3.connect('bot.db')
users = sql_connection()
timetable = sql_connection()
cursorUsr = users.cursor()
cursorTim = timetable.cursor()

# список групп для проверки существует ли указанная пользователем группа
grouplist = ["420-1", "420-2", "420-3", "420-4"]


# меню со статичными кнопками в поле ввода
# сообщения

@bot.on.private_message(payload={"cmd": "menu"})
async def keyboard_handler(message: Message):
    keyboard = Keyboard()
    keyboard.add(Text("На сегодня", {"cmd": "today"}))
    keyboard.add(Text("На завтра", {"cmd": "tomorrow"}))
    keyboard.row()
    keyboard.add(Text("На эту неделю", {"cmd": "thisweek"}))
    keyboard.add(Text("На следующую неделю", {"cmd": "nextweek"}))
    keyboard.row()
    keyboard.add(Text("Настройки", {"cmd": "settings"}))
    await message.answer("Выберите, на ", keyboard=keyboard)


# хэндлеры с отправкой пользователю расписания
# на выбранный день/период

@bot.on.private_message(payload={"cmd": "today"})
async def today_handler(message: Message):
    i = await bot.api.users.get(message.from_id)
    cursorUsr.execute("SELECT group_name FROM users WHERE user_id = ?", (i[0].id, ))
    group = cursorUsr.fetchone()
    text = get_schedule(group, 'today')
    await message.answer("Расписание на сегодня("+group[0]+"): \n\n"+text)
    #


@bot.on.private_message(payload={"cmd": "tomorrow"})
async def tommorow_handler(message: Message):
    i = await bot.api.users.get(message.from_id)
    cursorUsr.execute("SELECT group_name FROM users WHERE user_id = ?", (i[0].id,))
    group = cursorUsr.fetchone()
    text = get_schedule(group, 'tomorrow')
    await message.answer("Расписание на завтра("+group[0]+"):\n\n"+text)
    #


@bot.on.private_message(payload={"cmd": "thisweek"})
async def thisweek_handler(message: Message):
    i = await bot.api.users.get(message.from_id)
    cursorUsr.execute("SELECT group_name FROM users WHERE user_id = ?", (i[0].id,))
    group = cursorUsr.fetchone()
    text = get_schedule(group, 'thisweek')
    await message.answer("Расписание на эту неделю("+group[0]+"):\n\n"+text)


@bot.on.private_message(payload={"cmd": "nextweek"})
async def nextweek_handler(message: Message):
    i = await bot.api.users.get(message.from_id)
    cursorUsr.execute("SELECT group_name FROM users WHERE user_id = ?", (i[0].id,))
    group = cursorUsr.fetchone()
    text = get_schedule(group, 'nextweek')
    await message.answer("Расписание на следующую неделю("+group[0]+"):\n\n"+text)


# хэндлеры с подпиской пользователя на рассылку
# и отпиской тоже

@bot.on.private_message(payload={"cmd": "sub"})
async def sub_handler(message: Message, group=None):
    # добавление долбоёба в базу
    i = await bot.api.users.get(message.from_id)
    cursorUsr.execute("""UPDATE users SET subscribe = 'yes' WHERE user_id = ?""", (i[0].id, ))
    users.commit()
    await message.answer("Вы успешно подписались на рассылку")


@bot.on.private_message(payload={"cmd": "unsub"})
async def unsub_handler(message: Message):
    # удаление нищего дауна из базы данных тут
    i = await bot.api.users.get(message.from_id)
    cursorUsr.execute("""UPDATE users SET subscribe = 'no' WHERE user_id = ?""",
                      (i[0].id,))
    users.commit()
    await message.answer("Вы успешно отписались от рассылки")


# меню с настройками

@bot.on.private_message(payload={"cmd": "settings"})
async def settings_handler(message: Message):
    keyboard = Keyboard()
    keyboard.add(Text("Подписаться на рассылку", {"cmd": "sub"}))
    keyboard.row()
    keyboard.add(Text("Отписаться от рассылки", {"cmd": "unsub"}))
    keyboard.row()
    keyboard.add(Text("Изменить номер группы", {"cmd": "askgroup"}))
    keyboard.row()
    keyboard.add(Text("Вернуться в меню", {"cmd": "menu"}))
    await message.answer("Что вы хотите сделать?", keyboard=keyboard)


# приветственное сообщение и регистрация пользователя

@bot.on.message(text=["start", "начать"])
async def askgroup_handler(message: Message):
    await message.answer(
        "Привет! Чтобы начать работу, укажите номер своей группы через команду 'группа (номер_группы)'.",
        keyboard=EMPTY_KEYBOARD
    )
    await message.answer(
        "В дальнейшем это можно будет сделать в любой момент с помощью соответствующей команды, либо вызвать подсказку через меню настроек."
    )


# вылезает когда пользователь в настойках выбирает изменить свою группу

@bot.on.private_message(payload={"cmd": "askgroup"})
async def askgroup_handler(message: Message):
    await message.answer("Чтобы изменить номер группы, введите команду 'группа (номер_группы)'.")


# ввод группы, проверка существует ли она

@bot.on.private_message(
    text=["группа <group>", "group"]
)  # group принимает значение которое вводит пользователь после команды "группа ". group нужно вставлять в бд соответственно id пользователя
async def store_handler(message: Message, group=None):
    if group in grouplist:
        keyboard = Keyboard()
        keyboard.add(Text("Продолжить", {"cmd": "menu"}))
        users_info = await bot.api.users.get(
            message.from_id
        )

        insert_user(users_info, group, 'no')
        # вставка пользователя в таблицу(id, group, subscribe)
        # получается каждый раз, когда он будет "менять группу", он будет менять свой id... Пока не вижу как это исправить(или все равно)

        await message.answer("Изменения сохранены!", keyboard=keyboard)
    else:
        await message.answer("Такой группы не существует, либо вы указали аргумент пустым...")


# тестовая функция, позже уберу. оставила чтобы был пример как бот берет id пользователя

@bot.on.message(text="Привет")
async def hi_handler(ans: Message):
    users_info = await bot.api.users.get(ans.from_id)  # bot.api.users.get(ans.from_id) - бот собирает id пользователя. его нужно будет вставить в бд когда кто-то пишет "старт"
    await ans.answer("Привет, {}".format(users_info[0].first_name))


if __name__ == '__main__':
    bot.run_forever()
