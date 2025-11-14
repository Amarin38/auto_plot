from typing import List

from sqlalchemy import select

from domain.entities.services.prevision_data import PrevisionData
from infrastructure import SessionDB, db_engine
from infrastructure.db.models.services.prevision_data_model import PrevisionDataModel
from infrastructure.mappers.services.prevision_data_mapper import PrevisionDataMapper


class PrevisionDataRepository:
    def __init__(self) -> None:
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[PrevisionData]) -> None:
        with self.session as session:
            for e in entities:
                model = PrevisionDataMapper.to_model(e)
                session.add(model)
                session.commit()

    # Read -------------------------------------------
    def get_all(self) -> List[PrevisionData]:
        with self.session as session:
            models = session.scalars(
                select(PrevisionDataModel)
            ).all()

            return [PrevisionDataMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> PrevisionData:
        with self.session as session:
            model = session.scalars(
                select(PrevisionDataModel)
            ).filter(
                PrevisionDataModel.id == _id
            ).first()

            return PrevisionDataMapper.to_entity(model)


    def get_by_tipo_repuesto(self, tipo_rep: str) -> List[PrevisionData]:
        with self.session as session:
            model = session.scalars(
                select(PrevisionDataModel)
                .where(PrevisionDataModel.TipoRepuesto == tipo_rep)
            ).all()

            return [PrevisionDataMapper.to_entity(m) for m in model]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(PrevisionDataModel, _id)
                if row:
                    session.delete(row)