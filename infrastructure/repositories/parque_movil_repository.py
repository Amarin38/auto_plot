from typing import List

from sqlalchemy import select

from domain.entities.parque_movil import ParqueMovil
from infrastructure import SessionDB, db_engine
from infrastructure.db.models.parque_movil_model import ParqueMovilModel
from infrastructure.mappers.parque_movil_mapper import ParqueMovilMapper
from interfaces.repository import Repository


class ParqueMovilRepository(Repository):
        def __init__(self):
            self.session = SessionDB()
            self.engine = db_engine

        # Create -------------------------------------------
        def insert_many(self, entities: List[ParqueMovil]) -> None:
            with self.session as session:
                for e in entities:
                    model = ParqueMovilMapper.to_model(e)
                    session.add(model)
                    session.commit()

        # Read -------------------------------------------
        def get_all(self) -> List[ParqueMovil]:
            with self.session as session:
                models = session.scalars(
                    select(ParqueMovilModel)
                ).all()

                return [ParqueMovilMapper.to_entity(m) for m in models]

        def get_by_id(self, _id: int) -> ParqueMovil:
            with self.session as session:
                model = session.scalars(
                    select(ParqueMovilModel)
                ).filter(
                    ParqueMovilModel.id == _id
                ).first()

                return ParqueMovilMapper.to_entity(model)

        # Delete -------------------------------------------
        def delete_by_id(self, _id: int) -> None:
            with self.session as session:
                with session.begin():
                    row = session.get(ParqueMovilModel, _id)
                    if row:
                        session.delete(row)