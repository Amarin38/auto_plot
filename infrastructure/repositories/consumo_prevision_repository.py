from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.consumo_prevision import ConsumoPrevision
from infrastructure.db.models.consumo_prevision_model import ConsumoPrevisionModel
from infrastructure.mappers.consumo_prevision_mapper import ConsumoPrevisionMapper


class ConsumoPrevisionRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConsumoPrevision]) -> None:
        models = [ConsumoPrevisionMapper.to_model(e) for e in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[ConsumoPrevision]:
        models = self.session.scalars(
            select(ConsumoPrevisionModel)
        ).all()

        return [ConsumoPrevisionMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> ConsumoPrevision:
        model = self.session.scalars(
            select(ConsumoPrevisionModel).where(ConsumoPrevisionModel.id == _id)
        ).first()

        return ConsumoPrevisionMapper.to_entity(model)


    def get_by_tipo_repuesto(self, tipo_rep: str) -> List[ConsumoPrevision]:
        model = self.session.scalars(
            select(ConsumoPrevisionModel)
            .where(ConsumoPrevisionModel.TipoRepuesto == tipo_rep)
        ).all()

        return [ConsumoPrevisionMapper.to_entity(m) for m in model]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(ConsumoPrevisionModel, _id)
        if row:
            self.session.delete(row)

