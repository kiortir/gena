from tortoise import Tortoise

TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": ["repository.profile", "aerich.models"],
            "default_connection": "default",
        },
    },
}

async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(config=TORTOISE_ORM)
    #     await Tortoise.init(
    #     db_url='sqlite://db.sqlite3',
    #     modules={'models': ['repository.profile', "aerich.models"]}
    # )
    # Generate the schema
    await Tortoise.generate_schemas()
