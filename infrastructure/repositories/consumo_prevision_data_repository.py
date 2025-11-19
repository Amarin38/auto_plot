from typing import List

from sqlalchemy import select

from domain.entities.consumo_prevision_data import ConsumoPrevisionData
from infrastructure import SessionDB, db_engine
from infrastructure.db.models.consumo_prevision_data_model import ConsumoPrevisionDataModel
from infrastructure.mappers.consumo_prevision_data_mapper import ConsumoPrevisionDataMapper


class ConsumoPrevisionDataRepository:
    def __init__(self) -> None:
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConsumoPrevisionData]) -> None:
        with self.session as session:
            for e in entities:
                model = ConsumoPrevisionDataMapper.to_model(e)
                session.add(model)
                session.commit()

    # Read -------------------------------------------
    def get_all(self) -> List[ConsumoPrevisionData]:
        with self.session as session:
            models = session.scalars(
                select(ConsumoPrevisionDataModel)
            ).all()

            return [ConsumoPrevisionDataMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> ConsumoPrevisionData:
        with self.session as session:
            model = session.scalars(
                select(ConsumoPrevisionDataModel)
            ).filter(
                ConsumoPrevisionDataModel.id == _id
            ).first()

            return ConsumoPrevisionDataMapper.to_entity(model)


    def get_by_tipo_repuesto(self, tipo_rep: str) -> List[ConsumoPrevisionData]:
        with self.session as session:
            model = session.scalars(
                select(ConsumoPrevisionDataModel)
                .where(ConsumoPrevisionDataModel.TipoRepuesto == tipo_rep)
            ).all()

            return [ConsumoPrevisionDataMapper.to_entity(m) for m in model]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(ConsumoPrevisionDataModel, _id)
                if row:
                    session.delete(row)