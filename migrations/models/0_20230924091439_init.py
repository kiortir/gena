from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "hobby" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS "zodiac" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(8) NOT NULL UNIQUE
);
COMMENT ON COLUMN "zodiac"."name" IS 'Овен: Овен\nТелец: Телец\nБлизнецы: Близнецы\nРак: Рак\nЛев: Лев\nДева: Дева\nВесы: Весы\nСкорпион: Скорпион\nСтрелец: Стрелец\nКозерог: Козерог\nВодолей: Водолей\nРыбы: Рыбы';
CREATE TABLE IF NOT EXISTS "profile" (
    "telegram_id" SERIAL NOT NULL PRIMARY KEY,
    "telegram_tag" VARCHAR(255) NOT NULL UNIQUE,
    "name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    "birthday" DATE NOT NULL,
    "sex" VARCHAR(1) NOT NULL,
    "zodiac_id" INT NOT NULL REFERENCES "zodiac" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "profile"."sex" IS 'Male: M\nFemale: F';
CREATE TABLE IF NOT EXISTS "image" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "image_id" VARCHAR(255) NOT NULL UNIQUE,
    "profile_id" INT NOT NULL REFERENCES "profile" ("telegram_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "ack" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "u1_reaction" BOOL,
    "u2_reaction" BOOL,
    "u1_id" INT NOT NULL REFERENCES "profile" ("telegram_id") ON DELETE CASCADE,
    "u2_id" INT NOT NULL REFERENCES "profile" ("telegram_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "preferences" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "sex" VARCHAR(1),
    "profile_id" INT NOT NULL UNIQUE REFERENCES "profile" ("telegram_id") ON DELETE CASCADE
);
COMMENT ON COLUMN "preferences"."sex" IS 'Male: M\nFemale: F';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "hobby_profile" (
    "hobby_id" INT NOT NULL REFERENCES "hobby" ("id") ON DELETE CASCADE,
    "profile_id" INT NOT NULL REFERENCES "profile" ("telegram_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "preference_zodiac" (
    "zodiac_id" INT NOT NULL REFERENCES "zodiac" ("id") ON DELETE CASCADE,
    "preferences_id" INT NOT NULL REFERENCES "preferences" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
