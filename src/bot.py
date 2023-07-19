# 1. Не пересохраняет в базу данных данные при повторной регистрации -> сделать, что если tg_ID имеется в BD -> /reg -> Вы уже зареганы
# 2. На все сообщения (кроме команд) отвечает -> пришли фото --> Этап регистрации не заканчивается


import asyncio
from entity.profile import Profile
from repository.profile import Profile as ProfileDB
from repository.crud import get_profile
from aiogram import Bot, Dispatcher, types, executor
from db import init
from typing import TypedDict
import json
from redis_db import init_redis, redis_client
from registration import storage
from src.registration import _registration as reg

bot = Bot(token='6283819374:AAGYYlbtKO1D2AWXRrAVmR__t1mM5cNehKw')
dp = Dispatcher(bot)
reg_manager: reg.RegistrationManager = None # type: ignore

@dp.message_handler(commands=['reg'])
async def registration(message: types.Message):
    await reg_manager.start_registration(message)

@dp.message_handler(commands=['from_user'])
async def from_user(message: types.Message):
    await message.answer(message.from_user)

@dp.message_handler(commands=['me'])
async def me(message: types.Message):
    p = await get_profile(message.from_id)
    if p is None:
        await message.answer("Мы тебя не знаем")
        return
    info = f'Имя: {p.name}\nФамилия: {p.last_name}\nДень рождение: {p.birthday}\nПол: {p.sex.value}\nГород: {p.gorod} \nИщет: {p.kogo_ishu.value}'
    if p.photo != None: await message.answer_photo(p.photo, info) #p.telegram_tag
    else: await message.answer(info)

    # Реализация поиска людей:
    # когда (1) ищет (N): сколько лет (N) | кого ищу (пол) (1) | город (N)
    # когда пользователь ввел команду /find -> (беск-ый цикл) -> ищем всех пользователей который подходят
    # под наши критерии -> после вывода пользователю (1) пользователя (N) -> добовляем пользователя (N)
    # в новую таблицу в базе данных которая будет очищаться спустя некоторое время

@dp.message_handler(commands=['edit'])
async def edit(message: types.Message):
    from src.registration._registration import SIGN_UP_STEPS, RegistrationManager
    for el in SIGN_UP_STEPS:
        await message.answer(f'Будешь менять {el.field}? (Yes/No)')
        if message.text.lower() == 'yes':
            await message.answer(f'Введи новое заничение {el.field}')
            #RegistrationManager.save_profile() #TODO: написать фун-ию кот-ая будет по el.field сохранять данные (в случае если их меняют)
        else: continue


@dp.message_handler(regexp=r".+", content_types=['any'])
async def process_message(message: types.Message) -> None:
    # signing_up = await reg_manager.continue_registration(message) # edit, reg
    # if signing_up:
    #     return
    chat_id = message.chat.id
    text = message.text
    await bot.send_message(chat_id, f'Вы написали: {text}')
    return None

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет! Это мой первый бот на Aiogram.")


async def main():
    await init()
    client = await init_redis()
    context_storage = storage.RedisStorage(redis_client=client)
    global reg_manager
    reg_manager = reg.RegistrationManager(context_storage)
    
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
        executor.start_polling(dp, skip_updates=True)
    finally:
        if redis_client:
            loop.run_until_complete(redis_client.close())
