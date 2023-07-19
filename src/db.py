from tortoise import Tortoise

TORTOISE_ORM = {
    "connections": {"default": "asyncpg://postgres:postgres@postgres-bot:5432/postgres"},
    "apps": {
        "models": {
            "models": ["repository.profile", "aerich.models"],
            "default_connection": "default",
        },
    },
}

async def init():
    await Tortoise.init(config=TORTOISE_ORM)
