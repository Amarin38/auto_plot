from typing import List

from sqlalchemy import select

from domain.entities.conteo_stock import ConteoStock
from infrastructure import SessionDB, db_engine
from infrastructure.db.models.conteo_stock_model import ConteoStockModel
from infrastructure.mappers.conteo_stock_mapper import ConteoStockMapper


class ConteoStockRepository:
    def __init__(self) -> None:
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConteoStock]) -> None:
        with self.session as session:
            for e in entities:
                model = ConteoStockMapper.to_model(e)
                session.add(model)
                session.commit()


    # Read -------------------------------------------
    def get_all(self) -> List[ConteoStock]:
        with self.session as session:
            models = session.scalars(
                select(ConteoStockModel)
            ).all()

            return [ConteoStockMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> ConteoStock:
        with self.session as session:
            model = session.scalars(
                select(ConteoStockModel)
            ).filter(
                ConteoStockModel.id == _id
            ).first()

            return ConteoStockMapper.to_entity(model)

    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(ConteoStockModel, _id)
                if row:
                    session.delete(row)