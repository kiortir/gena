from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "profile" (
    "telegram_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    "age" INT NOT NULL,
    "sex" VARCHAR(6) NOT NULL  /* MALE: male\nFEMALE: female */,
    "gorod" TEXT NOT NULL,
    "kogo_ishu" VARCHAR(6) NOT NULL  /* MALE: male\nFEMALE: female */,
    "photo" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "acknowledged" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "acknowledged_by_id" INT NOT NULL REFERENCES "profile" ("telegram_id") ON DELETE CASCADE,
    "acknowledged_who_id" INT NOT NULL REFERENCES "profile" ("telegram_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
