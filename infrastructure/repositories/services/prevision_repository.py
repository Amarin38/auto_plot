from typing import List

from sqlalchemy import select

from domain.entities.services.prevision import Prevision
from infrastructure import SessionServices, services_engine
from infrastructure.db.models.services.prevision_model import PrevisionModel
from infrastructure.mappers.services.prevision_mapper import PrevisionMapper


class PrevisionRepository:
    def __init__(self) -> None:
        self.session = SessionServices()
        self.engine = services_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[Prevision]) -> None:
        with self.session as session:
            for e in entities:
                model = PrevisionMapper.to_model(e)
                session.add(model)
                session.commit()

    # Read -------------------------------------------
    def get_all(self) -> List[Prevision]:
        with self.session as session:
            models = session.scalars(
                select(PrevisionModel)
            ).all()

            return [PrevisionMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> Prevision:
        with self.session as session:
            model = session.scalars(
                select(PrevisionModel)
            ).filter(
                PrevisionModel.id == _id
            ).first()

            return PrevisionMapper.to_entity(model)


    def get_by_tipo_repuesto(self, tipo_rep: str) -> List[Prevision]:
        with self.session as session:
            model = session.scalars(
                select(PrevisionModel)
                .where(PrevisionModel.TipoRepuesto == tipo_rep)
            ).all()

            return [PrevisionMapper.to_entity(m) for m in model]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(PrevisionModel, _id)
                if row:
                    session.delete(row)

