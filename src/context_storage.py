from abc import ABC, abstractmethod
from flow_entity import Flow

class StorageBase(ABC):
    
    @abstractmethod
    def get(self, user_id: int) -> Flow:
        ...
    
    @abstractmethod
    def set(self, user_id: int, value: Flow) -> Flow:
        ...