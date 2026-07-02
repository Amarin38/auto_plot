from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.consumo.prevision import ConsumoPrevision
from infrastructure.db.models.consumo.prevision_model import ConsumoPrevisionModel
from infrastructure.mapper import Mapper


class ConsumoPrevisionRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConsumoPrevision]) -> None:
        models = [Mapper.to_model(entity, ConsumoPrevision) for entity in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[ConsumoPrevision]:
        models = self.session.scalars(
            select(ConsumoPrevisionModel)
        ).all()

        return [Mapper.to_entity(model, ConsumoPrevision) for model in models]


    def get_by_id(self, _id: int) -> ConsumoPrevision:
        model = self.session.scalars(
            select(ConsumoPrevisionModel).where(ConsumoPrevisionModel.id == _id)
        ).first()

        return Mapper.to_entity(model, ConsumoPrevision)


    def get_by_tipo_repuesto(self, tipo_rep: str) -> List[ConsumoPrevision]:
        models = self.session.scalars(
            select(ConsumoPrevisionModel)
            .where(ConsumoPrevisionModel.TipoRepuesto == tipo_rep)
        ).all()

        return [Mapper.to_entity(model, ConsumoPrevision) for model in models]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(ConsumoPrevisionModel, _id)
        if row:
            self.session.delete(row)

