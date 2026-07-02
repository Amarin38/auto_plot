from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select, delete

from domain.entities.datos.repuestos_codigos import RepuestosCodigos
from infrastructure.db.models.datos.repuestos_codigos_model import RepuestosCodigosModel
from infrastructure.mapper import Mapper


class RepuestosCodigosRepository:
    def __init__(self, session: Session):
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[RepuestosCodigos]) -> None:
        self.delete_all()
        models = [Mapper.to_model(entity, RepuestosCodigosModel) for entity in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[RepuestosCodigos]:
        models = self.session.scalars(
            select(RepuestosCodigosModel)
        ).all()

        return [Mapper.to_entity(model, RepuestosCodigos) for model in models]


    def get_by_id(self, _id: int) -> RepuestosCodigos:
        model = self.session.scalars(
            select(RepuestosCodigosModel).where(RepuestosCodigosModel.id == _id)
        ).first()

        return Mapper.to_entity(model, RepuestosCodigos)


    def get_by_codigo_repuesto(self, codigo: str) -> RepuestosCodigos:
        model = self.session.scalars(
            select(RepuestosCodigosModel).where(RepuestosCodigosModel.Codigos == codigo)
        ).first()

        return Mapper.to_entity(model, RepuestosCodigos)

    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(RepuestosCodigosModel, _id)
        if row:
            self.session.delete(row)


    def delete_all(self) -> None:
        self.session.execute(delete(RepuestosCodigosModel))
        self.session.commit()
