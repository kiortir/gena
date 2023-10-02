from tortoise.connection import connections
from tortoise.expressions import Q

from repository.entity.utils import Sex
from repository.models.hobby import Hobby
from repository.models.profile import Profile, Image
from repository.models.preferences import Zodiac, Preferences


from schema.profile_schema import (
    ProfileCreate,
    ProfileUpdate,
    Profile as ProfileSchema,
)
from repository.models.ack import Ack


class HobbyManager:
    @staticmethod
    async def create(name: str) -> Hobby:
        return await Hobby.create(name=name)

    @staticmethod
    async def read(id: int) -> Hobby:
        return await Hobby.get(id=id)

    @staticmethod
    async def update(id: int, name: str) -> Hobby:
        await Hobby.filter(id=id).update(name=name)
        updated = await Hobby.get(id=id)
        return updated

    @staticmethod
    async def delete(id: int) -> int:
        return await Hobby.filter(id=id).delete()

    @staticmethod
    async def read_many(
        limit: int | None = None, offset: int | None = None
    ) -> list[Hobby]:
        q_coro = Hobby.all()
        if limit:
            q_coro = q_coro.limit(limit)
            if offset:
                q_coro = q_coro.offset(offset)

        return await q_coro

    @staticmethod
    async def delete_many(*ids: int) -> list[int]:
        hobby = await Hobby.filter(id__in=ids).delete()
        print(hobby)
        return list(ids)


class ProfileManager:
    @staticmethod
    async def create(profile: ProfileCreate) -> Profile:
        profileDB = await Profile.create(
            zodiac=(await Zodiac.get(name=profile.zodiac)),
            **profile.model_dump(exclude={"zodiac"}),
        )
        return profileDB

    @staticmethod
    async def read(id: int) -> ProfileSchema:
        p = await Profile.get(telegram_id=id).prefetch_related("zodiac")
        return ProfileSchema.model_validate(p, from_attributes=True)

    @staticmethod
    async def update(id: int, profile: ProfileUpdate) -> ProfileSchema:
        values = profile.model_dump(exclude_none=True, exclude={"zodiac"})
        if profile.zodiac:
            values["zodiac"] = await Zodiac.get(name=profile.zodiac)
        await Profile.filter(telegram_id=id).update(**values)
        updated = await Profile.get(telegram_id=id).prefetch_related("zodiac")
        return ProfileSchema.model_validate(updated, from_attributes=True)

    @staticmethod
    async def delete(id: int) -> int:
        return await Profile.filter(telegram_id=id).delete()

    @staticmethod
    async def read_many(
        limit: int | None = None, offset: int | None = None
    ) -> list[ProfileSchema]:
        q_coro = Profile.all().prefetch_related("zodiac")
        if limit:
            q_coro = q_coro.limit(limit)
            if offset:
                q_coro = q_coro.offset(offset)

        return [
            ProfileSchema.model_validate(p, from_attributes=True)
            for p in (await q_coro)
        ]

    @staticmethod
    async def delete_many(*ids: int) -> list[int]:
        await Profile.filter(telegram_id__in=ids).delete()
        return list(ids)


class PreferenceManager:
    @staticmethod
    async def create_preference(
        telegram_id: int, sex: Sex, zodiac_ids: list[int]
    ) -> Preferences:
        preference = await Preferences.create(profile_id=telegram_id, sex=sex)
        await preference.zodiacs.add(
            *[z for z in await Zodiac.filter(id__in=zodiac_ids)]
        )
        return preference

    @staticmethod
    async def delete_preference(telegram_id: int) -> int:
        preference = await Preferences.filter(profile_id=telegram_id).delete()
        return preference

    @staticmethod
    async def update_preference(
        tg_id: int, sex: Sex, zodiac_ids: list[int]
    ) -> Preferences:
        await PreferenceManager.delete_preference(tg_id)
        preference = await PreferenceManager.create_preference(
            telegram_id=tg_id, sex=sex, zodiac_ids=zodiac_ids
        )
        return preference

    @staticmethod
    async def get_suggestion(profile_id: int) -> Profile | None:
        profile = await Profile.get(telegram_id=profile_id).prefetch_related("preferences")
        zodiacs = [zodiac.id for zodiac in profile.preferences.zodiacs]
        if not profile:
            return None
        
        q = Profile.filter(
            ~Q(acked_second__u1_id=profile_id) 
            & ~Q(
                Q(acked_first__u2_id=profile_id),
                Q(acked_first__u1_reaction=False),
                join_type="AND",
            ),
        )
        q = q.filter(Q(zodiac__id__in=zodiacs) & Q(sex=profile.preferences.sex))
        return await q.first()


class ImageManager:
    @staticmethod
    async def create_images(
        profile_id: int, image_ids: list[str]
    ) -> list[Image]:
        images = await Image.bulk_create(
            [
                Image(profile_id=profile_id, image_id=image_id)
                for image_id in image_ids
            ]
        )
        return images  # type: ignore

    @staticmethod
    async def purge_images(profile_id: int) -> int:
        image = await Image.filter(profile_id=profile_id).delete()
        return image

    @staticmethod
    async def set_images(
        profile_id: int, image_ids: list[str]
    ) -> list[Image]:
        await ImageManager.purge_images(profile_id)
        images = await ImageManager.create_images(profile_id, image_ids)
        return images


class AckManager:
    @staticmethod
    async def create_ack(u1_id: int, u2_id: int, reaction: bool) -> Ack | None:
        """Метод вызывается тогда, когда одна из сторон лайкнула другую."""

        conn = connections.get("default")

        await conn.execute_query(
            """
                INSERT INTO ack (u1_id, u2_id, u1_reaction) VALUES (?, ?, ?)
                    ON CONFLICT DO UPDATE SET u2_reaction = ?
                    WHERE ack.u2_id = ? and u1_id = ?
                """,
            [u1_id, u2_id, reaction, reaction, u1_id, u2_id],
        )

        return None


# 1) /repository/model/preference -- добавить возможность привязывать / обновлять предпочтения ✅
# 2) /repository/model/profile -- добавитить возможность добавлять фото (purge, add) ✅
# 2) /repository/model/ack -- добавить возможность добавления записей в таблицу ack ✅
