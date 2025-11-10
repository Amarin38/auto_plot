from typing import List

from sqlalchemy import select

from domain.entities.services.distribucion_normal import DistribucionNormal
from infrastructure import SessionServices, services_engine
from infrastructure.db.models.services.distribucion_normal_model import DistribucionNormalModel
from infrastructure.mappers.services.distribucion_normal_mapper import DistribucionNormalMapper


class DistribucionNormalRepository:
    def __init__(self) -> None:
        self.session = SessionServices()
        self.engine = services_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[DistribucionNormal]) -> None:
        with self.session as session:
            for e in entities:
                model = DistribucionNormalMapper.to_model(e)
                session.add(model)
                session.commit()


    # Read -------------------------------------------
    def get_all(self) -> List[DistribucionNormal]:
        with self.session as session:
            models = session.scalars(
                select(DistribucionNormalModel)
            ).all()

            return [DistribucionNormalMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> DistribucionNormal:
        with self.session as session:
            model = session.scalars(
                select(DistribucionNormalModel)
            ).filter(
                DistribucionNormalModel.id == _id
            ).first()

            return DistribucionNormalMapper.to_entity(model)


    def get_by_repuesto(self, repuesto: str) -> List[DistribucionNormal]:
        with self.session as session:
            models = session.scalars(
                select(DistribucionNormalModel)
                .where(DistribucionNormalModel.Repuesto == repuesto)
            ).all()

            return [DistribucionNormalMapper.to_entity(m) for m in models]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(DistribucionNormalModel, _id)
                if row:
                    session.delete(row)