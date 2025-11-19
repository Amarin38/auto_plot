import datetime
from typing import List

from sqlalchemy import select, func

from domain.entities.garantias_datos import GarantiasDatos
from infrastructure import SessionDB, db_engine
from infrastructure.db.models.garantias_datos_model import GarantiasDatosModel
from infrastructure.mappers.garantias_datos_mapper import GarantiasDatosMapper
from interfaces.repository import Repository


class GarantiasDatosRepository(Repository):
    def __init__(self) -> None:
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[GarantiasDatos]) -> None:
        with self.session as session:
            for e in entities:
                model = GarantiasDatosMapper.to_model(e)
                session.add(model)
                session.commit()

    # Read -------------------------------------------
    def get_all(self) -> List[GarantiasDatos]:
        with self.session as session:
            models = session.scalars(
                select(GarantiasDatosModel)
            ).all()

            return [GarantiasDatosMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> GarantiasDatos:
        with self.session as session:
            model = session.scalars(
                select(GarantiasDatosModel)
            ).filter(
                GarantiasDatosModel.id == _id
            ).first()

            return GarantiasDatosMapper.to_entity(model)


    def get_min_date(self) -> datetime.date:
        with self.session as session:
            return session.query(
                func.min(GarantiasDatosModel.FechaIngreso)
            ).scalar()


    def get_max_date(self) -> datetime.date:
        with self.session as session:
            return session.query(
                func.max(GarantiasDatosModel.FechaIngreso)
            ).scalar()



    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(GarantiasDatosModel, _id)
                if row:
                    session.delete(row)