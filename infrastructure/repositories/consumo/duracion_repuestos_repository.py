from typing import List

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.consumo.duracion_repuestos import DuracionRepuestos
from infrastructure.db.models.consumo.duracion_repuestos_model import DuracionRepuestosModel
from infrastructure.mapper import Mapper


class DuracionRepuestosRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[DuracionRepuestos]) -> None:
        models = [Mapper.to_model(entity, DuracionRepuestosModel) for entity in entities]
        self.session.add_all(models)

    # Read -------------------------------------------
    def get_all(self) -> List[DuracionRepuestos]:
        models = self.session.scalars(
            select(DuracionRepuestosModel)
        ).all()

        return [Mapper.to_entity(model, DuracionRepuestos) for model in models]


    def get_by_id(self, _id: int) -> DuracionRepuestos:
        model = self.session.scalars(
            select(DuracionRepuestosModel).where(DuracionRepuestosModel.id == _id)
        ).first()

        return Mapper.to_entity(model, DuracionRepuestos)


    def get_by_repuesto(self, repuesto: str) -> List[DuracionRepuestos]:
        models = self.session.scalars(
            select(DuracionRepuestosModel)
            .where(DuracionRepuestosModel.Repuesto == repuesto)
        ).all()

        return [Mapper.to_entity(model, DuracionRepuestos) for model in models]


    def get_repuestos(self) -> pd.Series:
        model = self.session.scalars(
            select(DuracionRepuestosModel.Repuesto).distinct()
        ).all()
        return pd.Series(model)


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(DuracionRepuestosModel, _id)
        if row:
            self.session.delete(row)