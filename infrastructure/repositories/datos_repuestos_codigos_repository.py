from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select, delete

from domain.entities.datos_repuestos_codigos import RepuestosCodigos
from infrastructure.db.models.datos_repuestos_codigos_model import RepuestosCodigosModel
from infrastructure.mappers.datos_repuestos_codigos_mapper import RepuestosCodigosMapper
from interfaces.repository import Repository


class RepuestosCodigosRepository(Repository):
    def __init__(self, session: Session):
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[RepuestosCodigos]) -> None:
        self.delete_all()
        models = [RepuestosCodigosMapper.to_model(e) for e in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[RepuestosCodigos]:
        models = self.session.scalars(
            select(RepuestosCodigosModel)
        ).all()

        return [RepuestosCodigosMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> RepuestosCodigos:
        model = self.session.scalars(
            select(RepuestosCodigosModel).where(RepuestosCodigosModel.id == _id)
        ).first()

        return RepuestosCodigosMapper.to_entity(model)


    def get_by_codigo_repuesto(self, codigo: str) -> RepuestosCodigos:
        model = self.session.scalars(
            select(RepuestosCodigosModel).where(RepuestosCodigosModel.Codigos == codigo)
        ).first()

        return RepuestosCodigosMapper.to_entity(model)

    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(RepuestosCodigosModel, _id)
        if row:
            self.session.delete(row)


    def delete_all(self) -> None:
        self.session.execute(delete(RepuestosCodigosModel))
        self.session.commit()
