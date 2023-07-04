from entity.profile import Profile
from repository.profile import Profile as ProfileDB
from aiogram import Bot, Dispatcher, types, executor
from db import init
from typing import TypedDict

bot = Bot(token='6283819374:AAGYYlbtKO1D2AWXRrAVmR__t1mM5cNehKw')
dp = Dispatcher(bot)

class RegistrationStatus(TypedDict):
    step: int
    data: dict[str, str]

REGISTRATION_STATUSES: dict[int, RegistrationStatus]
REGISTRATION_STEPS = []

@dp.message_handler(commands=['reg']) # сделать хорошо
async def process_start_command_2(message: types.Message):
    # await message.reply("Привет, введи данные.")
    REGISTRATION_STATUSES[message.from_id] = RegistrationStatus(step=-1, data={})
    
    
@dp.message_handler(regexp=r".+")
async def process_message(message: types.Message):
    chat_id = message.chat.id
    text = message.text
    await bot.send_message(chat_id, f'Вы написали: {text}')

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет! Это мой первый бот на Aiogram.")


async def main():
    await init()
    my_profile = Profile(age=17, name='Gena', last_name='Chubakov', sex='male', gorod='Moscow', #type: ignore
                         kogo_ishu='female', telegram_id=32489328947389279, photo='https://yandex.ru') #type: ignore
    my_profileDB = ProfileDB(**my_profile.dict())
    await my_profileDB.save()   
    print(await ProfileDB.all())

if __name__ == '__main__':
    # import asyncio
    # asyncio.run(main())
    executor.start_polling(dp, skip_updates=True)
