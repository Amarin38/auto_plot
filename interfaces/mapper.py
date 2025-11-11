from abc import ABC, abstractmethod
from typing import Any


class Mapper(ABC):
    @staticmethod
    @abstractmethod
    def to_entity(model: Any) -> Any:
        pass

    @staticmethod
    @abstractmethod
    def to_model(entity: Any) -> Any:
        pass