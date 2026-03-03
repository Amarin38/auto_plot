from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from config.enums import RepuestoEnum
from domain.entities.consumo_desviacion_indices import ConsumoDesviacionIndices
from infrastructure.db.models.consumo_desviacion_indices_model import ConsumoDesviacionIndicesModel
from infrastructure.mappers.consumo_desviacion_indices_mapper import ConsumoDesviacionIndicesMapper


class ConsumoDesviacionIndicesRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConsumoDesviacionIndices]) -> None:
        models = [ConsumoDesviacionIndicesMapper.to_model(e) for e in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[ConsumoDesviacionIndices]:
        models = self.session.scalars(
            select(ConsumoDesviacionIndicesModel)
        ).all()

        return [ConsumoDesviacionIndicesMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> ConsumoDesviacionIndices:
        model = self.session.scalars(
            select(ConsumoDesviacionIndicesModel).where(ConsumoDesviacionIndicesModel.id == _id)
        ).first()

        return ConsumoDesviacionIndicesMapper.to_entity(model)


    def get_by_tipo_rep(self, tipo_rep: RepuestoEnum) -> List[ConsumoDesviacionIndices]:
        models = self.session.scalars(
            select(ConsumoDesviacionIndicesModel)
            .where(ConsumoDesviacionIndicesModel.TipoRepuesto == tipo_rep)
        ).all()

        return [ConsumoDesviacionIndicesMapper.to_entity(m) for m in models]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(ConsumoDesviacionIndicesModel, _id)
        if row:
            self.session.delete(row)


    def delete(self) -> None:
        self.session.query(ConsumoDesviacionIndicesModel).delete()
