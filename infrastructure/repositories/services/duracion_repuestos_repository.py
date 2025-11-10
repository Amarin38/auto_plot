from typing import List

from sqlalchemy import select

from domain.entities.services.duracion_repuestos import DuracionRepuestos
from infrastructure import SessionServices, services_engine
from infrastructure.db.models.services.duracion_repuestos_model import DuracionRepuestosModel
from infrastructure.mappers.services.duracion_repuestos_mapper import DuracionRepuestosMapper


class DuracionRepuestosRepository:
    def __init__(self) -> None:
        self.session = SessionServices()
        self.engine = services_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[DuracionRepuestos]) -> None:
        with self.session as session:
            for e in entities:
                model = DuracionRepuestosMapper.to_model(e)
                session.add(model)
                session.commit()


    # Read -------------------------------------------
    def get_all(self) -> List[DuracionRepuestos]:
        with self.session as session:
            models = session.scalars(
                select(DuracionRepuestosModel)
            ).all()

            return [DuracionRepuestosMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> DuracionRepuestos:
        with self.session as session:
            model = session.scalars(
                select(DuracionRepuestosModel)
            ).filter(
                DuracionRepuestosModel.id == _id
            ).first()

            return DuracionRepuestosMapper.to_entity(model)


    def get_by_repuesto(self, repuesto: str) -> List[DuracionRepuestos]:
        with self.session as session:
            models = session.scalars(
                select(DuracionRepuestosModel)
                .where(DuracionRepuestosModel.Repuesto == repuesto)
            ).all()

            return [DuracionRepuestosMapper.to_entity(m) for m in models]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(DuracionRepuestosModel, _id)
                if row:
                    session.delete(row)