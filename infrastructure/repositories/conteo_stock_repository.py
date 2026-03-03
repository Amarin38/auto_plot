from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.conteo_stock import ConteoStock
from infrastructure.db.models.conteo_stock_model import ConteoStockModel
from infrastructure.mappers.conteo_stock_mapper import ConteoStockMapper


class ConteoStockRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConteoStock]) -> None:
        models = [ConteoStockMapper.to_model(e) for e in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[ConteoStock]:
        models = self.session.scalars(
            select(ConteoStockModel)
        ).all()

        return [ConteoStockMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> ConteoStock:
        model = self.session.scalars(
            select(ConteoStockModel).where(ConteoStockModel.id == _id)
        ).first()

        return ConteoStockMapper.to_entity(model)


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(ConteoStockModel, _id)
        if row:
            self.session.delete(row)