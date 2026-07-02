from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.inicio_conteo_stock import ConteoStock
from infrastructure.db.models.inicio_conteo_stock_model import ConteoStockModel
from infrastructure.mapper import Mapper


class ConteoStockRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConteoStock]) -> None:
        models = [Mapper.to_model(entity, ConteoStockModel) for entity in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[ConteoStock]:
        models = self.session.scalars(
            select(ConteoStockModel)
        ).all()

        return [Mapper.to_entity(model, ConteoStock) for model in models]


    def get_by_id(self, _id: int) -> ConteoStock:
        model = self.session.scalars(
            select(ConteoStockModel).where(ConteoStockModel.id == _id)
        ).first()

        return Mapper.to_entity(model, ConteoStock)


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(ConteoStockModel, _id)
        if row:
            self.session.delete(row)