from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session
from domain.entities.datos.maximos_minimos import MaximosMinimos
from infrastructure.db.models.datos.maximos_minimos_model import MaximosMinimosModel
from infrastructure.mapper import Mapper


class MaximosMinimosRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[MaximosMinimos]) -> None:
        models = [Mapper.to_model(entity, MaximosMinimosModel) for entity in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[MaximosMinimos]:
        models = self.session.scalars(
            select(MaximosMinimosModel)
        ).all()

        return [Mapper.to_entity(model, MaximosMinimos) for model in models]


    def get_by_id(self, _id: int) -> MaximosMinimos:
        model = self.session.scalars(
            select(MaximosMinimosModel).where(MaximosMinimosModel.id == _id)
        ).first()

        return Mapper.to_entity(model, MaximosMinimos)


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(MaximosMinimosModel, _id)
        if row:
            self.session.delete(row)