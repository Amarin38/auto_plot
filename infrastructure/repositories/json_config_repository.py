from typing import List

from multipledispatch import dispatch
from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.json_config import JSONConfig
from infrastructure.db.models.json_config_model import JSONConfigModel
from infrastructure.mappers.json_config_mapper import JSONConfigMapper
from interfaces.repository import Repository


class JSONConfigRepository(Repository):
    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[JSONConfig]) -> None:
        models = [JSONConfigMapper.to_model(e) for e in entities]
        self.session.add_all(models)

    # Read -------------------------------------------
    def get_all(self) -> List[JSONConfig]:
        models = self.session.scalars(
            select(JSONConfigModel)
        ).all()

        return [JSONConfigMapper.to_entity(m) for m in models]


    @dispatch(int)
    def get_by_id(self, _id: int) -> JSONConfig:
        model = self.session.scalars(
            select(JSONConfigModel).where(JSONConfigModel.id == _id)
        ).first()

        return JSONConfigMapper.to_entity(model)


    @dispatch(str)
    def get_by_id(self, nombre: str) -> JSONConfig:
        model = self.session.scalars(
            select(JSONConfigModel).where(JSONConfigModel.nombre == nombre)
        ).first()

        return JSONConfigMapper.to_entity(model)


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(JSONConfigModel, _id)
        if row:
            self.session.delete(row)