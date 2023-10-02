from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

TOKEN = '6568631440:AAHQNa9lKtbzR0vDlxED7-jIQ00yh3N8mJI'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)

@dp.message_handler(content_types=['text'])
async def all_message(message: types.Message):
    ...

@dp.message_handler(commands=['register'])
async def message(message: types.Message):
    ...

if __name__ == '__main__':
    executor.start_polling(dp)

