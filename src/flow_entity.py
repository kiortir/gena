from typing import Type, Any, Callable, Generic, TypeVar


from enum import IntEnum, auto
from pydantic import BaseModel


class ValidationError(Exception):
    ...

class FlowState(IntEnum):
    NAME_SELECTION = auto()
    LAST_NAME_SELECTION = auto()
    BIRTHDAY_SELECTION = auto()
    SEX_SELECTION = auto()
    PHOTOS_SELECTION = auto()
    PREFERENCES_SELECTION = auto()
    # ...


class Flow(BaseModel):
    state: FlowState
    end_state: FlowState
    current_step: FlowState

    values: Any