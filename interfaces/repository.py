from abc import ABC, abstractmethod
from typing import List, Any


class Repository(ABC):
    # Create -------------------------------------------
    @abstractmethod
    def insert_many(self, entities: List[Any]) -> None:
        pass


    # Read -------------------------------------------
    @abstractmethod
    def get_all(self) -> List[Any]:
        pass

    @abstractmethod
    def get_by_id(self, _id: int) -> Any:
        pass


    # Delete -------------------------------------------
    @abstractmethod
    def delete_by_id(self, _id: int) -> None:
        pass