from typing import List

from sqlalchemy import select

from domain.entities.consumo_desviacion_indices import ConsumoDesviacionIndices
from infrastructure import SessionDB, db_engine
from infrastructure.db.models.consumo_desviacion_indices_model import ConsumoDesviacionIndicesModel
from infrastructure.mappers.consumo_desviacion_indices_mapper import ConsumoDesviacionIndicesMapper


class ConsumoDesviacionIndicesRepository:
    def __init__(self) -> None:
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConsumoDesviacionIndices]) -> None:
        with self.session as session:
            for e in entities:
                model = ConsumoDesviacionIndicesMapper().to_model(e)
                session.add(model)
                session.commit()


    # Read -------------------------------------------
    def get_all(self) -> List[ConsumoDesviacionIndices]:
        with self.session as session:
            models = session.scalars(
                select(ConsumoDesviacionIndicesModel)
            ).all()

            return [ConsumoDesviacionIndicesMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> ConsumoDesviacionIndices:
        with self.session as session:
            model = session.scalars(
                select(ConsumoDesviacionIndicesModel)
            ).filter(
                ConsumoDesviacionIndicesModel.id == _id
            ).first()

            return ConsumoDesviacionIndicesMapper.to_entity(model)


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(ConsumoDesviacionIndicesModel, _id)
                if row:
                    session.delete(row)