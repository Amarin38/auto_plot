from typing import TypeVar, Type

from pydantic import BaseModel

SQLALCH = TypeVar("SQLALCH") # Clase de SQLAlchemy
PYD     = TypeVar("PYD", bound=BaseModel) # Clase de Pydantic

class Mapper:
    @staticmethod
    def to_entity(model: SQLALCH, entity: Type[PYD]) -> PYD:
        return entity.model_validate(model)

    @staticmethod
    def to_model(entity: PYD, model: Type[SQLALCH]) -> SQLALCH:
        return model(**entity.model_dump(exclude_none=True))

