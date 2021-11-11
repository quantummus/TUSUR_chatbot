from vkbottle.bot import Bot, Message
from vkbottle import LoopWrapper

bot = Bot("ba11cc5d4ee4bd92628131613bc774856efcb57c2b89b44295941c51ca249da41c22fd69fae0f61aabd32")
bot.labeler.vbml_ignore_case = True

grouplist = ["420-1", "420-2", "420-3", "420-4"]

@bot.on.message(text="Привет")
async def hi_handler(ans: Message):
    users_info = await bot.api.users.get(ans.from_id)
    await ans.answer("Привет, {}".format(users_info[0].first_name))

@bot.on.private_message(text="тест")
async def post_yes_handler(ans: Message):
    await ans.answer("В какой группе ты учишься?")
    @bot.on.private_message(text="<group>")
    async def echo_answer(ans: Message, group):
        if group in grouplist:
           await ans.answer("Ты учишься в %s группе" % (group))
        else:
            users_info = await bot.api.users.get(ans.from_id)
            await ans.answer("Нет такой группы, {}!".format(users_info[0].first_name))

lw = LoopWrapper()

@lw.interval(seconds=10)
async def repeated_task(ans: Message):
    await ans.answer("гав гав")

bot.run_forever()
