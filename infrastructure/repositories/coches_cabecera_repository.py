from typing import List

from sqlalchemy import select

from domain.entities.coches_cabecera import CochesCabecera
from infrastructure import SessionDB, db_engine
from infrastructure.db.models.coches_cabecera_model import CochesCabeceraModel
from infrastructure.mappers.coches_cabecera_mapper import CochesCabeceraMapper
from interfaces.repository import Repository


class CochesCabeceraRepository(Repository):
    def __init__(self) -> None:
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[CochesCabecera]) -> None:
        with self.session as session:
            for e in entities:
                model = CochesCabeceraMapper.to_model(e)
                session.add(model)
                session.commit()


    # Read -------------------------------------------
    def get_all(self) -> List[CochesCabecera]:
        with self.session as session:
            models = session.scalars(
                select(CochesCabeceraModel)
            ).all()

            return [CochesCabeceraMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> CochesCabecera:
        with self.session as session:
            model = session.scalars(
                select(CochesCabeceraModel)
            ).filter(
                CochesCabeceraModel.id == _id
            ).first()

            return CochesCabeceraMapper.to_entity(model)


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(CochesCabeceraModel, _id)
                if row:
                    session.delete(row)