from vkbottle.bot import Bot, Message
from vkbottle import LoopWrapper, Keyboard, KeyboardButtonColor, Text, EMPTY_KEYBOARD, BaseStateGroup
import asyncio

bot = Bot("ba11cc5d4ee4bd92628131613bc774856efcb57c2b89b44295941c51ca249da41c22fd69fae0f61aabd32")
bot.labeler.vbml_ignore_case = True

grouplist = ["420-1", "420-2", "420-3", "420-4"]

class UserState(BaseStateGroup):
    sub = 0
    group = 3

@bot.on.private_message(payload={"cmd": "menu"})
async def keyboard_handler(message: Message):
    keyboard = Keyboard()
    keyboard.add(Text("На сегодня", {"cmd": "today"}))
    keyboard.add(Text("На завтра", {"cmd": "tommorow"}))
    keyboard.row()
    keyboard.add(Text("На эту неделю", {"cmd": "thisweek"}))
    keyboard.add(Text("На следующую неделю", {"cmd": "nextweek"}))
    keyboard.row()
    keyboard.add(Text("Настройки", {"cmd": "settings"}))
    await message.answer("Выберите, на ", keyboard=keyboard)

@bot.on.private_message(payload={"cmd": "today"})

@bot.on.private_message(payload={"cmd": "tommorow"})

@bot.on.private_message(payload={"cmd": "thisweek"})

@bot.on.private_message(payload={"cmd": "nextweek"})

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

@bot.on.message(text=["start", "начать"])
async def askgroup_handler(message: Message):
    await message.answer("Привет! Чтобы начать работу, укажите номер своей группы через команду 'группа (номер_группы)'.", keyboard=EMPTY_KEYBOARD)
    await message.answer("В дальнейшем это можно будет сделать в любой момент с помощью соответствующей команды, либо вызвать подсказку через меню настроек.")

@bot.on.private_message(payload={"cmd": "askgroup"})
async def askgroup_handler(message: Message):
    await message.answer("Чтобы изменить номер группы, введите команду 'группа (номер_группы)'.")

@bot.on.private_message(text=["группа <group>", "group"])
async def store_handler(message: Message, group=None):
    if group in grouplist:
        keyboard = Keyboard()
        keyboard.add(Text("Продолжить", {"cmd": "menu"}))
        await message.answer("Изменения сохранены!", keyboard=keyboard)
    else:
        await message.answer("Такой группы не существует, либо вы указали аргумент пустым...")


@bot.on.message(text="Привет")
async def hi_handler(ans: Message):
    users_info = await bot.api.users.get(ans.from_id)
    await ans.answer("Привет, {}".format(users_info[0].first_name))

bot.run_forever()
