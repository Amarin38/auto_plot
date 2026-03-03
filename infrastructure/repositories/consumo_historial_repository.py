from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from config.enums import RepuestoEnum
from domain.entities.consumo_historial import ConsumoHistorial
from infrastructure.db.models.consumo_historial_model import ConsumoHistorialModel
from infrastructure.mappers.consumo_historial_mapper import ConsumoHistorialMapper
from interfaces.repository import Repository


class ConsumoHistorialRepository(Repository):
    def __init__(self, session: Session):
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConsumoHistorial]) -> None:
        models = [ConsumoHistorialMapper.to_model(e) for e in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[ConsumoHistorial]:
        models = self.session.scalars(
            select(ConsumoHistorialModel)
        ).all()

        return [ConsumoHistorialMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> ConsumoHistorial:
        model = self.session.scalars(
            select(ConsumoHistorialModel).where(ConsumoHistorialModel.id == _id)
        ).first()

        return ConsumoHistorialMapper.to_entity(model)


    def get_by_tipo_rep(self, tipo_repuesto: RepuestoEnum) -> List[ConsumoHistorial]:
        model = self.session.scalars(
            select(ConsumoHistorialModel)
            .where(ConsumoHistorialModel.TipoRepuesto == tipo_repuesto)
        )

        return [ConsumoHistorialMapper.to_entity(m) for m in model]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(ConsumoHistorialModel, _id)
        if row:
            self.session.delete(row)