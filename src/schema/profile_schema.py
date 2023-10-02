import datetime
from pydantic import BaseModel, computed_field
from repository.entity.utils import Sex, ZodiacOptions, ZODIAC_RANGES


class ProfileBase(BaseModel):
    telegram_id: int
    telegram_tag: str

    name: str
    last_name: str

    birthday: datetime.date
    sex: Sex

    @computed_field  # type: ignore[misc]
    @property
    def zodiac(self) -> ZodiacOptions | None:
        if not self.birthday:
            return None
        date, month = (
            self.birthday.day,
            self.birthday.month,
        )
        for sign in ZODIAC_RANGES:
            sign_name, daterange = sign
            start, end = daterange
            start_day, start_month = start
            end_day, end_month = end
            if start_month == month:
                if start_day <= date:
                    return sign_name
            if end_month == month:
                if end_day >= date:
                    return sign_name

        return None


class ProfileCreate(ProfileBase, BaseModel):
    ...


class ProfileUpdate(ProfileBase, BaseModel):
    telegram_id: int | None = None
    telegram_tag: str | None = None

    name: str | None = None
    last_name: str | None = None

    birthday: datetime.date | None = None
    sex: Sex | None = None


class Zodiac(BaseModel):
    id: int
    name: str


class Profile(BaseModel):
    telegram_id: int
    telegram_tag: str

    name: str
    last_name: str

    birthday: datetime.date
    sex: Sex

    zodiac: Zodiac
