from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from config.enums import RepuestoEnum
from domain.entities.consumo.historial import ConsumoHistorial
from infrastructure.db.models.consumo.historial_model import ConsumoHistorialModel
from infrastructure.mapper import Mapper


class ConsumoHistorialRepository:
    def __init__(self, session: Session):
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConsumoHistorial]) -> None:
        models = [Mapper.to_model(entity, ConsumoHistorialModel) for entity in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[ConsumoHistorial]:
        models = self.session.scalars(
            select(ConsumoHistorialModel)
        ).all()

        return [Mapper.to_entity(model, ConsumoHistorial) for model in models]


    def get_by_id(self, _id: int) -> ConsumoHistorial:
        model = self.session.scalars(
            select(ConsumoHistorialModel).where(ConsumoHistorialModel.id == _id)
        ).first()

        return Mapper.to_entity(model, ConsumoHistorial)


    def get_by_tipo_rep(self, tipo_repuesto: RepuestoEnum) -> List[ConsumoHistorial]:
        models = self.session.scalars(
            select(ConsumoHistorialModel)
            .where(ConsumoHistorialModel.TipoRepuesto == tipo_repuesto)
        )

        return [Mapper.to_entity(model, ConsumoHistorial) for model in models]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(ConsumoHistorialModel, _id)
        if row:
            self.session.delete(row)