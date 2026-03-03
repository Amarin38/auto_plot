from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.consumo_prevision_data import ConsumoPrevisionData
from infrastructure.db.models.consumo_prevision_data_model import ConsumoPrevisionDataModel
from infrastructure.mappers.consumo_prevision_data_mapper import ConsumoPrevisionDataMapper


class ConsumoPrevisionDataRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConsumoPrevisionData]) -> None:
        models = [ConsumoPrevisionDataMapper.to_model(e) for e in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[ConsumoPrevisionData]:
        models = self.session.scalars(
            select(ConsumoPrevisionDataModel)
        ).all()

        return [ConsumoPrevisionDataMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> ConsumoPrevisionData:
        model = self.session.scalars(
            select(ConsumoPrevisionDataModel).where(ConsumoPrevisionDataModel.id == _id)
        ).first()

        return ConsumoPrevisionDataMapper.to_entity(model)


    def get_by_tipo_repuesto(self, tipo_rep: str) -> List[ConsumoPrevisionData]:
        model = self.session.scalars(
            select(ConsumoPrevisionDataModel)
            .where(ConsumoPrevisionDataModel.TipoRepuesto == tipo_rep)
        ).all()

        return [ConsumoPrevisionDataMapper.to_entity(m) for m in model]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(ConsumoPrevisionDataModel, _id)
        if row:
            self.session.delete(row)