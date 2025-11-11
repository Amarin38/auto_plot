import datetime
from typing import List

from sqlalchemy import select, func

from domain.entities.common.datos_garantias import DatosGarantias
from infrastructure import SessionCommon, common_engine
from infrastructure.db.models.common.datos_garantias_model import DatosGarantiasModel
from infrastructure.mappers.common.datos_garantias_mapper import DatosGarantiasMapper
from interfaces.repository import Repository


class DatosGarantiasRepository(Repository):
    def __init__(self) -> None:
        self.session = SessionCommon()
        self.engine = common_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[DatosGarantias]) -> None:
        with self.session as session:
            for e in entities:
                model = DatosGarantiasMapper.to_model(e)
                session.add(model)
                session.commit()

    # Read -------------------------------------------
    def get_all(self) -> List[DatosGarantias]:
        with self.session as session:
            models = session.scalars(
                select(DatosGarantiasModel)
            ).all()

            return [DatosGarantiasMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> DatosGarantias:
        with self.session as session:
            model = session.scalars(
                select(DatosGarantiasModel)
            ).filter(
                DatosGarantiasModel.id == _id
            ).first()

            return DatosGarantiasMapper.to_entity(model)


    def get_min_date(self) -> datetime.date:
        with self.session as session:
            return session.query(
                func.min(DatosGarantiasModel.FechaIngreso)
            ).scalar()


    def get_max_date(self) -> datetime.date:
        with self.session as session:
            return session.query(
                func.max(DatosGarantiasModel.FechaIngreso)
            ).scalar()



    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(DatosGarantiasModel, _id)
                if row:
                    session.delete(row)