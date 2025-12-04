
from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    name: str

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def run(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        ...
