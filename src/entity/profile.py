from pydantic import BaseModel, AnyHttpUrl
from enum import Enum
import datetime

class Sex(str, Enum):
    MALE = 'male'
    FEMALE = 'female'

class Profile(BaseModel):
    telegram_id: int
    name: str
    last_name: str
    birthday: datetime.date
    sex: Sex
    gorod: str
    kogo_ishu: Sex
    photo: AnyHttpUrl

