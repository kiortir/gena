import asyncio
import logging
import sys

from tortoise import Tortoise

from repository.models.preferences import Zodiac, ZodiacOptions
from settings import PGSettings

fmt = logging.Formatter(
    fmt="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(fmt)

# will print debug sql
logger_db_client = logging.getLogger("tortoise.db_client")
logger_db_client.setLevel(logging.DEBUG)
logger_db_client.addHandler(sh)

logger_tortoise = logging.getLogger("tortoise")
logger_tortoise.setLevel(logging.DEBUG)
logger_tortoise.addHandler(sh)

database = PGSettings()  # type: ignore

TORTOISE_ORM = {
    "connections": {"default": database.url},
    "apps": {
        "models": {
            "models": [
                "repository.models.profile",
                "repository.models.ack",
                "repository.models.hobby",
                "repository.models.preferences",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}


async def init() -> None:
    await Tortoise.init(config=TORTOISE_ORM)
    await Zodiac.bulk_create((Zodiac(name=option.value) for option in ZodiacOptions), ignore_conflicts=True)
    return None


if __name__ == "__main__":
    asyncio.run(init())