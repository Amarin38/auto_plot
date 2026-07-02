from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.consumo.distribucion_normal import DistribucionNormal
from infrastructure.db.models.consumo.distribucion_normal_model import DistribucionNormalModel
from infrastructure.mapper import Mapper


class DistribucionNormalRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[DistribucionNormal]) -> None:
        models = [Mapper.to_model(entity, DistribucionNormalModel) for entity in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[DistribucionNormal]:
        models = self.session.scalars(
            select(DistribucionNormalModel)
        ).all()

        return [Mapper.to_entity(model, DistribucionNormal) for model in models]


    def get_by_id(self, _id: int) -> DistribucionNormal:
        model = self.session.scalars(
            select(DistribucionNormalModel).where(DistribucionNormalModel.id == _id)
        ).first()

        return Mapper.to_entity(model, DistribucionNormal)


    def get_by_repuesto(self, repuesto: str) -> List[DistribucionNormal]:
        models = self.session.scalars(
            select(DistribucionNormalModel)
            .where(DistribucionNormalModel.Repuesto == repuesto)
        ).all()

        return [Mapper.to_entity(model, DistribucionNormal) for model in models]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(DistribucionNormalModel, _id)
        if row:
            self.session.delete(row)