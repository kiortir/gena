import datetime
from enum import Enum
from typing import Literal

from pydantic import AnyHttpUrl, BaseModel, Field, RootModel

from entity.profile import Sex


class RegistrationData(BaseModel):
    name: str | None = None
    last_name: str | None = None
    birthday: datetime.date | None = None
    sex: Sex | None = None
    gorod: str | None = None
    kogo_ishu: Sex | None = None
    photo: str | None = None


class RegistrationEntry(BaseModel):
    
    data: RegistrationData = Field(default_factory=RegistrationData)
    step: int
    
class ContextType(str, Enum):
    EDIT = "edit"
    REG = "reg"
    
class EditContent(BaseModel):
    field: str
    
class BaseContext(BaseModel):
    type: ContextType
    content: RegistrationEntry | EditContent
    
class RegContext(BaseContext, BaseModel):
    type: Literal[ContextType.REG]
    content: RegistrationEntry
    
class EditContext(BaseContext, BaseModel):
    type: Literal[ContextType.EDIT]
    content: EditContent
    
Context = RootModel[RegContext | EditContext]

