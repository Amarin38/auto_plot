import datetime
from typing import List

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from domain.entities.garantias_datos import GarantiasDatos
from infrastructure.db.models.garantias_datos_model import GarantiasDatosModel
from infrastructure.mappers.garantias_datos_mapper import GarantiasDatosMapper
from interfaces.repository import Repository


class GarantiasDatosRepository(Repository):
    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[GarantiasDatos]) -> None:
        models = [GarantiasDatosMapper.to_model(e) for e in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[GarantiasDatos]:
        models = self.session.scalars(
            select(GarantiasDatosModel)
        ).all()

        return [GarantiasDatosMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> GarantiasDatos:
        model = self.session.scalars(
            select(GarantiasDatosModel).where(GarantiasDatosModel.id == _id)
        ).first()

        return GarantiasDatosMapper.to_entity(model)


    def get_min_date(self) -> datetime.date:
        return self.session.query(
            func.min(GarantiasDatosModel.FechaIngreso)
        ).scalar()


    def get_max_date(self) -> datetime.date:
        return self.session.query(
            func.max(GarantiasDatosModel.FechaIngreso)
        ).scalar()


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(GarantiasDatosModel, _id)
        if row:
            self.session.delete(row)