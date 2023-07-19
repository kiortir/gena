from enum import Enum
from typing import Any, Literal
from pydantic import BaseModel

class ContextType(str, Enum):
    REGISTRATION = "registration"
    EDIT = "edit"

class ContextBase(BaseModel):
    
    type: ContextType
    
    content: BaseModel
    
class RegContext(BaseModel):
    
    type: Literal[ContextType.REGISTRATION]
    content: Any

class EditContext(BaseModel):
    
    type: Literal[ContextType.EDIT]
    content: Any
    
from pydantic import RootModel

Context = RootModel[RegContext | EditContext]
context = Context(root=...).root
