from abc import ABC, abstractmethod
import json
from typing import Any, Callable


from entity import registration



class StorageBase(ABC):
          

    @abstractmethod
    async def get(self,telegram_id: int ) -> registration.Context | None:
        ...

        
    @abstractmethod
    async def set(self, telegram_id: int,  data: registration.Context) -> registration.Context:
        ...
        
    @abstractmethod
    async def done(self, telegram_id: int):
        ...


class RedisStorage(StorageBase):
    
    import redis.asyncio as redis
    
    def __init__(self, redis_client: "redis.Redis"):
        self.client = redis_client
    

    async def get(self, telegram_id: int) -> registration.Context | None:
        content: bytes | None = await self.client.get(str(telegram_id))
        if not content:            
            return None
        parsed_content = json.loads(content)
        entry = registration.Context(root=parsed_content)
        return entry
    
    async def set(self, telegram_id: int, entry: registration.Context):
        await self.client.set(str(telegram_id), entry.model_dump_json(), ex=3600)
        return entry
    
    async def done(self, telegram_id: int):
        await self.client.delete(str(telegram_id))
        
