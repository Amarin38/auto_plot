from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.consumo_duracion_repuestos import DuracionRepuestos
from infrastructure.db.models.consumo_duracion_repuestos_model import DuracionRepuestosModel
from infrastructure.mappers.consumo_duracion_repuestos_mapper import DuracionRepuestosMapper


class DuracionRepuestosRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[DuracionRepuestos]) -> None:
        models = [DuracionRepuestosMapper.to_model(e) for e in entities]
        self.session.add_all(models)

    # Read -------------------------------------------
    def get_all(self) -> List[DuracionRepuestos]:
        models = self.session.scalars(
            select(DuracionRepuestosModel)
        ).all()

        return [DuracionRepuestosMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> DuracionRepuestos:
        model = self.session.scalars(
            select(DuracionRepuestosModel).where(DuracionRepuestosModel.id == _id)
        ).first()

        return DuracionRepuestosMapper.to_entity(model)


    def get_by_repuesto(self, repuesto: str) -> List[DuracionRepuestos]:
        models = self.session.scalars(
            select(DuracionRepuestosModel)
            .where(DuracionRepuestosModel.Repuesto == repuesto)
        ).all()

        return [DuracionRepuestosMapper.to_entity(m) for m in models]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(DuracionRepuestosModel, _id)
        if row:
            self.session.delete(row)