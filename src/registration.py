from aiogram import types
import datetime
from entity import profile

async def process_name(message: types.Message, context: dict[str, dict[str, str] | int]):
    text = message.text
    context["data"]["name"] = text
    context["step"] += 1
    await message.reply(f"Привет, {text}. Какая у тебя фамилия?")
    
    
async def process_last_name(message: types.Message, context: dict[str, dict[str, str] | int]):
    text = message.text
    context["data"]["last_name"] = text
    context["step"] += 1
    await message.reply(f"Окей. Когда ты родился?")
    
async def process_birthday(message: types.Message, context: dict[str, dict[str, str] | int]):
    text = message.text
    try:
        a = datetime.datetime.strptime(text, '%d/%m/%Y')
    except Exception:
        await message.reply(f"Неправильная дата рождения")
        return
    
    context["data"]["birthday"] = a
    context["step"] += 1
    await message.reply(f"Окей. Когда ты родился? (Пример: 03/09/2006)")

async def process_sex(message: types.Message, context: dict[str, dict[str, str] | int]):
    text = message.text
    try:
        a = profile.Sex(text)
    except Exception:
        await message.reply('Неправильный пол')
        return
    context["data"]["sex"] = a
    context["step"] += 1
    await message.reply(f"Какой у тебя пол? (male, female)")
    
async def process_gorod(message: types.Message, context: dict[str, dict[str, str] | int]):
    text = message.text
    context["data"]["gorod"] = text
    context["step"] += 1
    await message.reply(f"Окей. С какого ты города?")
    
async def process_kogo_ishu(message: types.Message, context: dict[str, dict[str, str] | int]):
    text = message.text
    context["data"]["kogo_ishu"] = text
    context["step"] += 1
    await message.reply(f"Окей. Кого ты ищешь?")

async def process_photo(message: types.Message, context: dict[str, dict[str, str] | int]):
    text = message.text
    try:
        a = profile.AnyHttpUrl(text)
    except Exception:
        await message.reply('Неправильная фотка')
        return
    context["data"]["photo"] = a
    context["step"] += 1
    await message.reply(f"Окей. Пришли свое фото?")