from typing import List

from sqlalchemy import select

from domain.entities.services.maximos_minimos import MaximosMinimos
from infrastructure import SessionServices, services_engine
from infrastructure.db.models.services.maximos_minimos_model import MaximosMinimosModel
from infrastructure.mappers.services.maximos_minimos_mapper import MaximosMinimosMapper


class MaximosMinimosRepository:
    def __init__(self) -> None:
        self.session = SessionServices()
        self.engine = services_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[MaximosMinimos]) -> None:
        with self.session as session:
            for e in entities:
                model = MaximosMinimosMapper.to_model(e)
                session.add(model)
                session.commit()


    # Read -------------------------------------------
    def get_all(self) -> List[MaximosMinimos]:
        with self.session as session:
            models = session.scalars(
                select(MaximosMinimosModel)
            ).all()

            return [MaximosMinimosMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> MaximosMinimos:
        with self.session as session:
            model = session.scalars(
                select(MaximosMinimosModel)
            ).filter(
                MaximosMinimosModel.id == _id
            ).first()

            return MaximosMinimosMapper.to_entity(model)


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(MaximosMinimosModel, _id)
                if row:
                    session.delete(row)