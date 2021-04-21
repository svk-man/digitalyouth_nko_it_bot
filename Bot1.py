from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

#TOKEN = '1756077502:AAEW_cavIZErG8g6pCK_axKOafPtxNB--8s'

bot = Bot(token = '1756077502:AAEW_cavIZErG8g6pCK_axKOafPtxNB--8s')
dp = Dispatcher(bot)


@dp.message_handler (commands = ['start'])
async def process_start_command(message: types.Message):
    await message.reply('Приветствую! \nНапиши, что-нибудь для проверки!')
    
@dp.message_handler (commands = ['help'])
async def process_start_command(message: types.Message):
    await message.reply('Здесь выводится информация о боте и подсказки')
    
# Для общих сообщений
@dp.message_handler()
async def remes(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)
    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)
    
#asyncio.run(main())