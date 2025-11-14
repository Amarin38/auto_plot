from typing import List

from multipledispatch import dispatch
from sqlalchemy import select

from domain.entities.json_config import JSONConfig
from infrastructure import SessionDB, db_engine
from infrastructure.db.models.json_config_model import JSONConfigModel
from infrastructure.mappers.json_config_mapper import JSONConfigMapper
from interfaces.repository import Repository


class JSONConfigRepository(Repository):
    def __init__(self) -> None:
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[JSONConfig]) -> None:
        with self.session as session:
            for e in entities:
                model = JSONConfigMapper.to_model(e)
                session.add(model)
                session.commit()


    # Read -------------------------------------------
    def get_all(self) -> List[JSONConfig]:
        with self.session as session:
            models = session.scalars(
                select(JSONConfigModel)
            ).all()

            return [JSONConfigMapper.to_entity(m) for m in models]


    @dispatch(int)
    def get_by_id(self, _id: int) -> JSONConfig:
        with self.session as session:
            model = session.scalars(
                select(JSONConfigModel)
                .where(JSONConfigModel.id == _id)
            ).first()

            return JSONConfigMapper.to_entity(model)


    @dispatch(str)
    def get_by_id(self, nombre: str) -> JSONConfig:
        with self.session as session:
            model = session.scalars(
                select(JSONConfigModel)
                .where(JSONConfigModel.nombre == nombre)
            ).first()

            return JSONConfigMapper.to_entity(model)


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(JSONConfigModel, _id)
                if row:
                    session.delete(row)