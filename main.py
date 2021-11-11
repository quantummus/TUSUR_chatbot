from vkbottle.bot import Bot, Message
from vkbottle_types import BaseStateGroup
from vkbottle import LoopWrapper, Keyboard, KeyboardButtonColor, Text, EMPTY_KEYBOARD, CtxStorage

bot = Bot("ba11cc5d4ee4bd92628131613bc774856efcb57c2b89b44295941c51ca249da41c22fd69fae0f61aabd32")
bot.labeler.vbml_ignore_case = True

grouplist = ["420-1", "420-2", "420-3", "420-4"]

ctx = CtxStorage()

class UserInfo(BaseStateGroup):
    GROUP = 0
    GOTOMENU = 1

@bot.on.message(text="тыква")
@bot.on.message(state=UserInfo.GOTOMENU)
async def keyboard_handler(message: Message):
    keyboard = Keyboard()
    keyboard.add(Text("На сегодня", {"cmd": "today"}))
    keyboard.add(Text("На завтра", {"cmd": "tommorow"}))
    keyboard.row()
    keyboard.add(Text("На эту неделю", {"cmd": "thisweek"}))
    keyboard.add(Text("На следующую неделю", {"cmd": "nextweek"}))
    keyboard.row()
    keyboard.add(Text("Подписаться на рассылку"), color=KeyboardButtonColor.POSITIVE)
    keyboard.row()
    keyboard.add(Text("Изменить номер группы", {"cmd": "askgroup"}), color=KeyboardButtonColor.NEGATIVE)
    await message.answer("тыква", keyboard=keyboard)

@bot.on.message(text=["start", "начать работу"])
@bot.on.private_message(payload={"cmd": "askgroup"})
async def askgroup_handler(message: Message):
    await message.answer("В какой группе ты учишься?", keyboard=EMPTY_KEYBOARD)
    await bot.state_dispenser.set(message.peer_id, UserInfo.GROUP)

@bot.on.message(state=UserInfo.GROUP)
async def getgroup_answer(message: Message):
    if message.text in grouplist:
        await message.answer("Ты учишься в %s группе" % (message.text))
    else:
        users_info = await bot.api.users.get(message.from_id)
        await message.answer("Нет такой группы, {}!".format(users_info[0].first_name))


@bot.on.message(text="Привет")
async def hi_handler(ans: Message):
    users_info = await bot.api.users.get(ans.from_id)
    await ans.answer("Привет, {}".format(users_info[0].first_name))

bot.run_forever()
