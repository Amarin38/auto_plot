from typing import List

from sqlalchemy import select

from domain.entities.desviacion_indices import DesviacionIndices
from infrastructure import SessionDB, db_engine
from infrastructure.db.models.desviacion_indices_model import DesviacionIndicesModel
from infrastructure.mappers.desviacion_indices_mapper import DesviacionIndicesMapper


class DesviacionIndicesRepository:
    def __init__(self) -> None:
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[DesviacionIndices]) -> None:
        with self.session as session:
            for e in entities:
                model = DesviacionIndicesMapper().to_model(e)
                session.add(model)
                session.commit()


    # Read -------------------------------------------
    def get_all(self) -> List[DesviacionIndices]:
        with self.session as session:
            models = session.scalars(
                select(DesviacionIndicesModel)
            ).all()

            return [DesviacionIndicesMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> DesviacionIndices:
        with self.session as session:
            model = session.scalars(
                select(DesviacionIndicesModel)
            ).filter(
                DesviacionIndicesModel.id == _id
            ).first()

            return DesviacionIndicesMapper.to_entity(model)


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(DesviacionIndicesModel, _id)
                if row:
                    session.delete(row)