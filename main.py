from vkbottle.bot import Bot, Message
from vkbottle import LoopWrapper, Keyboard, KeyboardButtonColor, Text, OpenLink, Location, EMPTY_KEYBOARD, template_gen, TemplateElement

bot = Bot("ba11cc5d4ee4bd92628131613bc774856efcb57c2b89b44295941c51ca249da41c22fd69fae0f61aabd32")
bot.labeler.vbml_ignore_case = True

grouplist = ["420-1", "420-2", "420-3", "420-4"]

@bot.on.message(text="тест кнопки")
async def keyboard_handler(message: Message):
    keyboard = Keyboard()
    keyboard.add(Text("На сегодня"))
    keyboard.add(Text("На завтра"))
    keyboard.row()
    keyboard.add(Text("На эту неделю"))
    keyboard.add(Text("На следующую неделю"))
    keyboard.row()
    keyboard.add(Text("Подписаться на рассылку"), color=KeyboardButtonColor.POSITIVE)
    keyboard.row()
    keyboard.add(Text("Изменить номер группы", {"cmd": "getgroup"}), color=KeyboardButtonColor.NEGATIVE)
    await message.answer("тыква", keyboard=keyboard)

@bot.on.message(text="тест кнопки кыш")
async def nokeyboard_handler(message: Message):
    await message.answer("Тыквы нет!", keyboard=EMPTY_KEYBOARD)

@bot.on.private_message(text="тест группа")
@bot.on.private_message(payload={"cmd": "getgroup"})
async def group_handler(ans: Message):
    await message.answer("В какой группе ты учишься?", keyboard=EMPTY_KEYBOARD)
    @bot.on.private_message(text="<group>")
    async def echo_answer(ans: Message, group):
        if group in grouplist:
           await ans.answer("Ты учишься в %s группе" % (group))
        else:
            users_info = await bot.api.users.get(ans.from_id)
            await ans.answer("Нет такой группы, {}!".format(users_info[0].first_name))



@bot.on.message(text="Привет")
async def hi_handler(ans: Message):
    users_info = await bot.api.users.get(ans.from_id)
    await ans.answer("Привет, {}".format(users_info[0].first_name))

bot.run_forever()
