from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.gomeria_diferencia_mov_dep import GomeriaDiferenciaMovEntreDep
from infrastructure.db.models.gomeria_diferencia_mov_dep_model import \
    GomeriaDiferenciaMovEntreDepModel
from infrastructure.mappers.gomeria_diferencia_mov_dep_mapper import \
    GomeriaDiferenciaMovEntreDepMapper
from interfaces.repository import Repository


class GomeriaDiferenciaMovEntreDepRepository(Repository):
    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[GomeriaDiferenciaMovEntreDep]) -> None:
        models = [GomeriaDiferenciaMovEntreDepMapper.to_model(e) for e in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[GomeriaDiferenciaMovEntreDep]:
        models = self.session.scalars(
            select(GomeriaDiferenciaMovEntreDepModel)
        ).all()

        return [GomeriaDiferenciaMovEntreDepMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> GomeriaDiferenciaMovEntreDep:
        model = self.session.scalars(
            select(GomeriaDiferenciaMovEntreDepModel)
            .where(GomeriaDiferenciaMovEntreDepModel.id == _id)
        ).first()

        return GomeriaDiferenciaMovEntreDepMapper.to_entity(model)


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(GomeriaDiferenciaMovEntreDepModel, _id)
        if row:
            self.session.delete(row)