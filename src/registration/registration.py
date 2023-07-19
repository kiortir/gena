import datetime
from typing import Any, Awaitable, Callable, Type

from aiogram import types

from entity.profile import Profile, Sex, CityEnum
from entity.registration import RegistrationData, RegistrationEntry, Context, ContextType
from registration.storage import StorageBase
from repository.crud import create_or_update_profile

REGISTRATION_FUNCTION = Callable[[types.Message], Awaitable]

class StepHandler:
    
    def __init__(self, fn: REGISTRATION_FUNCTION, question: str, field: str,  tip: str | None = None) -> None:
        self.fn = fn
        self.question = question
        self.tip = tip or question
        self.field = field
        
    async def parse(self, message: types.Message) -> Any | None:
        parsed_value = await self.fn(message)
        return parsed_value



SIGN_UP_STEPS: list[StepHandler] = []


class RegistrationManager:
    
    def __init__(self, storage: StorageBase):
        self.storage = storage
        
    def get_step(self, entry: RegistrationEntry):
        step = entry.step
        if step == len(SIGN_UP_STEPS):
            raise ValueError()
        else:
            return SIGN_UP_STEPS[step]
    
    async def start_registration(self, message: types.Message ):
        telegram_id = message.from_user.id
        entry = await self.storage.set(telegram_id, Context(type=ContextType.REG, content=RegistrationEntry(step=0))) # type: ignore
        if not entry.root.type is ContextType.REG:
            raise ValueError()
        current_step = self.get_step(entry.root.content)
        await self.start_step(message, current_step)
        
    async def start_step(self, message: types.Message, step: StepHandler):
        await message.answer(step.question)
    
    async def continue_registration(self, message: types.Message) -> bool:
        telegram_id = message.from_user.id
        entry = await self.storage.get(telegram_id, Context(type=ContextType.REG, content=RegistrationEntry(step=0))) #type: ignore
        if not entry.root.type:
            return False
        current_step = self.get_step(entry.root.type)
        try:
            parsed_value = await current_step.parse(message)
        except ValueError:
            await message.reply(current_step.tip)
            return True
        setattr(entry.root.content.data, current_step.field, parsed_value)
        entry.step += 1
        print(entry.step, len(SIGN_UP_STEPS))
        if entry.step == len(SIGN_UP_STEPS):
            await self.save_profile(telegram_id, entry.data) #message.from_user.first_name
            await self.storage.done(telegram_id)
        else:
            await self.storage.set(telegram_id, entry)
            await self.start_step(message, self.get_step(entry))
        return True
            
    async def save_profile(self, telegram_id: int, r: RegistrationData):
        profile = Profile(telegram_id=telegram_id, **r.model_dump())
        await create_or_update_profile(profile)
        


def register_step(question: str, field: str, tip:str | None = None):
    
    def decorator(fn: REGISTRATION_FUNCTION):
        step = StepHandler(field=field, question=question, fn=fn, tip=tip)
        SIGN_UP_STEPS.append(step)
        
        return fn
    
    return decorator
        
@register_step(field="name", question="Как тебя зовут?", tip="В имени не должно быть цифр, символов, смайликов и пр.")
async def validate_name(message: types.Message) -> Any:
    message_text = message.text
    if not message_text.isalpha():
        raise ValueError()
    else: return message_text.capitalize()
    
@register_step(field="last_name", question="Напиши свою фамилию", tip="В фамилии не должно быть цифр, символов, смайликов и пр.")
async def validate_last_name(message: types.Message) -> Any:
    message_text = message.text
    if not message_text.isalpha():
        raise ValueError()
    else: return message_text.capitalize()
    
@register_step(field="birthday", question="Когда ты родился?", tip="Напиши дату в формате дд.мм.ГГГГ")
async def validate_birthday(message: types.Message) -> Any:
    message_text = message.text
    try:
        d, m, y = [int(t) for t in message_text.split(".")]
        birthday = datetime.date(y,m,d)
    except Exception:
        raise ValueError()
    
    return birthday

@register_step(field="sex", question="Укажи пол (М, Ж)")
async def validate_sex(message: types.Message) -> Any:
    message_text = message.text
    if message_text not in ("М", "Ж"):
        raise ValueError()
    return Sex.MALE if message_text == "М" else Sex.FEMALE

@register_step(field="gorod", question=f"Укажи город из списка: {[e.value for e in CityEnum]}")
async def validate_city(message: types.Message) -> Any:
    message_text = message.text
    try:
        return CityEnum(message_text)
    except Exception:
        raise ValueError()
    
@register_step(field="kogo_ishu", question=f"Кого ты ищешь (М, Ж)?")
async def validate_target(message: types.Message) -> Any:
    message_text = message.text
    if message_text not in ("М", "Ж"):
        raise ValueError()
    return Sex.MALE if message_text == "М" else Sex.FEMALE

@register_step(field="photo", question=f"Отправь своё фото (или напиши 'нет')")
async def validate_photo(message: types.Message) -> Any:
    print(message)
    if message.photo:
        first = message.photo[0]
        photo_id = first.file_id
        return photo_id
    elif message.text == "нет":
            return None
    else:
        raise ValueError()
    
    
