from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "profile" (
    "telegram_id" SERIAL NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    "birthday" DATE NOT NULL,
    "sex" VARCHAR(6) NOT NULL,
    "gorod" TEXT NOT NULL,
    "kogo_ishu" VARCHAR(6) NOT NULL,
    "photo" TEXT NOT NULL
);
COMMENT ON COLUMN "profile"."sex" IS 'MALE: male\nFEMALE: female';
COMMENT ON COLUMN "profile"."kogo_ishu" IS 'MALE: male\nFEMALE: female';
CREATE TABLE IF NOT EXISTS "acknowledged" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "acknowledged_by_id" INT NOT NULL REFERENCES "profile" ("telegram_id") ON DELETE CASCADE,
    "acknowledged_who_id" INT NOT NULL REFERENCES "profile" ("telegram_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
