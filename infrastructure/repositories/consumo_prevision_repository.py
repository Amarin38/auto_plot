from typing import List

from sqlalchemy import select

from domain.entities.consumo_prevision import ConsumoPrevision
from infrastructure import SessionDB, db_engine
from infrastructure.db.models.consumo_prevision_model import ConsumoPrevisionModel
from infrastructure.mappers.consumo_prevision_mapper import ConsumoPrevisionMapper


class ConsumoPrevisionRepository:
    def __init__(self) -> None:
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConsumoPrevision]) -> None:
        with self.session as session:
            for e in entities:
                model = ConsumoPrevisionMapper.to_model(e)
                session.add(model)
                session.commit()

    # Read -------------------------------------------
    def get_all(self) -> List[ConsumoPrevision]:
        with self.session as session:
            models = session.scalars(
                select(ConsumoPrevisionModel)
            ).all()

            return [ConsumoPrevisionMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> ConsumoPrevision:
        with self.session as session:
            model = session.scalars(
                select(ConsumoPrevisionModel)
            ).filter(
                ConsumoPrevisionModel.id == _id
            ).first()

            return ConsumoPrevisionMapper.to_entity(model)


    def get_by_tipo_repuesto(self, tipo_rep: str) -> List[ConsumoPrevision]:
        with self.session as session:
            model = session.scalars(
                select(ConsumoPrevisionModel)
                .where(ConsumoPrevisionModel.TipoRepuesto == tipo_rep)
            ).all()

            return [ConsumoPrevisionMapper.to_entity(m) for m in model]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(ConsumoPrevisionModel, _id)
                if row:
                    session.delete(row)

