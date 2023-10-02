import datetime
from enum import Enum, IntEnum, auto
from typing import Any, Callable, Generic, Literal, Type, TypeVar

from aiogram.types import Message

from flow_entity import Flow, FlowState, ValidationError
from repository.entity.utils import Sex

from context_storage import StorageBase
T = TypeVar("T")


class FlowStep(Generic[T]):
    def __init__(
        self,
        state_element: FlowState,
        message: str,
        field: str,
        validators: list[Callable[[Message], None]],
        cast_fn: Callable[[Message], T],
    ) -> None:
        self.message = message
        self.field = field
        self.validators = validators
        self.cast_fn = cast_fn
        steps[state_element] = self

    def parse(self, value: Message) -> T:
        for validator in self.validators:
            validator(value)
        return self.cast_fn(value)
    
    @staticmethod
    def from_state(state: FlowState) -> "FlowStep":
        return steps[state]


steps: dict[FlowState, FlowStep[Any]] = {}


def has_body(value: Message) -> None:
    if not value.text:
        raise ValidationError("Сообщение должно содержать текст")
    return None

def is_valid_date_format(value: Message) -> None:
    try: 
        datetime.datetime.strptime(value.text, "%d.%m.%Y").date()
    except ValueError:
        raise ValidationError("Введите дату в формате ДД.ММ.ГГГГ")
    return None

def not_future(value: Message) -> None:
    if not datetime.datetime.strptime(value.text, "%d.%m.%Y").date() < datetime.date.today():
        raise ValidationError("Вы не можете быть из будущего")
    return None

def is_element_of_enum(value: Message, _type: Type[Enum]) -> None:
    try:
        _type(value.text)
    except ValueError:
        raise ValidationError(f"Введите значения из: {''.join([x.value for x in Sex])}")
    return None

FlowStep[str](
    state_element=FlowState.NAME_SELECTION,
    message="Введите своё имя",
    field="name",
    validators=[has_body],
    cast_fn=lambda x: x.text,
)

FlowStep[str](
    state_element=FlowState.LAST_NAME_SELECTION,
    message="Введите свою фамилию",
    field="last_name",
    validators=[has_body],
    cast_fn=lambda x: x.text,
)

FlowStep[datetime.date](
    state_element=FlowState.BIRTHDAY_SELECTION,
    message="Введите свою дату рождения",
    field="birthday",
    validators=[has_body, is_valid_date_format, not_future],
    cast_fn=lambda x: datetime.datetime.strptime(x.text, "%d.%m.%Y").date()
)


FlowStep[Sex](
    state_element=FlowState.SEX_SELECTION,
    message="Введите свой пол [М, Ж]",
    field="sex",
    validators=[has_body, lambda x: is_element_of_enum(x, Sex)], 
    cast_fn=lambda x: Sex(x.text)
)

class FlowManager:
    
    def __init__(self, storage: StorageBase):
        self.storage = storage
    
    def match_steps(self,  context: Literal["register"] | Literal["preferences"]) -> tuple[FlowState, FlowState]:
        
        if context == "register":
            return FlowState.NAME_SELECTION, FlowState.PREFERENCES_SELECTION
        elif context == "preferences":
            return FlowState.PREFERENCES_SELECTION, FlowState.PREFERENCES_SELECTION
        
    async def notify(self, message: Message, content: str) -> None:
        await message.answer(content)
        
    # async def is_not_context(self, context: Literal["register"] | Literal["preferences"], message: Message) -> None:
    #     if Flow.current_step is None:
    #         await self.start_context(context, message)
            
        
    async def start_context(self, context: Literal["register"] | Literal["preferences"], message: Message) -> None:
        start, end = self.match_steps(context)
        
        flow = Flow(state=start, end_state=end, current_step=start, values={})
        await self.notify(message, FlowStep.from_state(flow.current_step).message)
        self.storage.set(user_id=message.from_user.id, value=flow)

        # ловится register задаем начальный и конечный step
        # далее curr_step приравниваем к start_step
        # далее запускаем flow_step он смотрит current_step и в зависимости от него 
        # выводит сообщения. После вывода ожидаем сообщение от пользователя.
        # После получания сообщения, проверяем на корректность и сравниваем cur_step с end_step
        # Если они не равны -> cur_step увеличиваем, иначе останавливаем регистрацию.