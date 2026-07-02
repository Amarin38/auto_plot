from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.gomeria.diferencia_mov_dep import GomeriaDiferenciaMovEntreDep
from infrastructure.db.models.gomeria.diferencia_mov_dep_model import \
    GomeriaDiferenciaMovEntreDepModel
from infrastructure.mapper import Mapper


class GomeriaDiferenciaMovEntreDepRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[GomeriaDiferenciaMovEntreDep]) -> None:
        models = [Mapper.to_model(entity, GomeriaDiferenciaMovEntreDepModel) for entity in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[GomeriaDiferenciaMovEntreDep]:
        models = self.session.scalars(
            select(GomeriaDiferenciaMovEntreDepModel)
        ).all()

        return [Mapper.to_entity(model, GomeriaDiferenciaMovEntreDep) for model in models]


    def get_by_id(self, _id: int) -> GomeriaDiferenciaMovEntreDep:
        model = self.session.scalars(
            select(GomeriaDiferenciaMovEntreDepModel)
            .where(GomeriaDiferenciaMovEntreDepModel.id == _id)
        ).first()

        return Mapper.to_entity(model, GomeriaDiferenciaMovEntreDep)


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(GomeriaDiferenciaMovEntreDepModel, _id)
        if row:
            self.session.delete(row)