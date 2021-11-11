from vkbottle.bot import Bot, Message
import asyncio
from vkbottle import LoopWrapper

bot = Bot("ba11cc5d4ee4bd92628131613bc774856efcb57c2b89b44295941c51ca249da41c22fd69fae0f61aabd32")
bot.labeler.vbml_ignore_case = True

@bot.on.message(text="Привет")
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    await message.answer("Привет, {}".format(users_info[0].first_name))

@bot.on.message(text="Подписаться на рассылку")
async def post_yes_handler(message: Message):
    await message.answer("Вы успешно подписались на рассылку, но её пока что еще нет.")

@bot.on.message(text="Отписаться от рассылки")
async def post_no_handler(message: Message):
    await message.answer("Вы успешно отписались нот рассылки, но какой был в этом смысл, если она и так пока еще не существует?")

@bot.on.private_message(text="<msg>")
async def echo_answer(ans: Message, msg):
    await ans.answer("Ты написал: %s"%(msg))

lw = LoopWrapper()

@lw.interval(seconds=10)
async def repeated_task():
    await Message.answer("гав гав")

bot.run_forever()
