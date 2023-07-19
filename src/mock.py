from tortoise import Tortoise, fields, run_async
from tortoise.models import Model
from tortoise.transactions import in_transaction
from db import init
from repository import profile
from profile import Profile


async def get_all_profile():
    profiles = await profile.Profile.all()
    return profiles


async def add_profile():
    new_profile = await profile.Profile.create(
        name="Gennadiy",
        telegram_id=1234,
        last_name="hd",
        birthday="2010-03-03",
        sex=profile.Sex.MALE,
        gorod="Mos",
        kogo_ishu=profile.Sex.FEMALE,
        photo="https://yandex.ru",
    )

    return new_profile


"""
    telegram_id = fields.IntField(pk=True)
    name = fields.TextField()
    last_name = fields.TextField()
    birthday = fields.DateField()
    sex = fields.CharEnumField(Sex)
    gorod = fields.TextField()
    kogo_ishu = fields.CharEnumField(Sex) 
    photo = fields.TextField()
"""


async def main():
    await init()
    # await add_profile()
    print(await get_all_profile())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
