from typing import List

from sqlalchemy import select

from domain.entities.gomeria_diferencia_mov_dep import GomeriaDiferenciaMovEntreDep
from infrastructure import db_engine, SessionDB
from infrastructure.db.models.gomeria_diferencia_mov_dep_model import \
    GomeriaDiferenciaMovEntreDepModel
from infrastructure.mappers.gomeria_diferencia_mov_dep_mapper import \
    GomeriaDiferenciaMovEntreDepMapper
from interfaces.repository import Repository


class GomeriaDiferenciaMovEntreDepRepository(Repository):
    def __init__(self) -> None:
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[GomeriaDiferenciaMovEntreDep]) -> None:
        with self.session as session:
            for e in entities:
                model = GomeriaDiferenciaMovEntreDepMapper.to_model(e)
                session.add(model)
                session.commit()


    # Read -------------------------------------------
    def get_all(self) -> List[GomeriaDiferenciaMovEntreDep]:
        with self.session as session:
            models = session.scalars(
                select(GomeriaDiferenciaMovEntreDepModel)
            ).all()

            return [GomeriaDiferenciaMovEntreDepMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> GomeriaDiferenciaMovEntreDep:
        with self.session as session:
            model = session.scalars(
                select(GomeriaDiferenciaMovEntreDepModel)
            ).filter(
                GomeriaDiferenciaMovEntreDepModel.id == _id
            ).first()

            return GomeriaDiferenciaMovEntreDepMapper.to_entity(model)


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(GomeriaDiferenciaMovEntreDepModel, _id)
                if row:
                    session.delete(row)