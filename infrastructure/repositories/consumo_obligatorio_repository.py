from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from config.enums import ConsumoObligatorioEnum
from domain.entities.consumo_obligatorio import ConsumoObligatorio
from infrastructure.db.models.consumo_obligatorio_model import ConsumoObligatorioModel
from infrastructure.mappers.consumo_obligatorio_mapper import ConsumoObligatorioMapper
from interfaces.repository import Repository


class ConsumoObligatorioRepository(Repository):
    def __init__(self, session: Session):
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConsumoObligatorio]) -> None:
        models = [ConsumoObligatorioMapper.to_model(e) for e in entities]
        self.session.add_all(models)

    # Read -------------------------------------------
    def get_all(self) -> List[ConsumoObligatorio]:
        models = self.session.scalars(
            select(ConsumoObligatorioModel)
        ).all()

        return [ConsumoObligatorioMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> ConsumoObligatorio:
        model = self.session.scalars(
            select(ConsumoObligatorioModel).where(ConsumoObligatorioModel.id == _id)
        ).first()

        return ConsumoObligatorioMapper.to_entity(model)


    def get_by_repuesto(self, repuesto: ConsumoObligatorioEnum) -> List[ConsumoObligatorio]:
        models = self.session.scalars(
            select(ConsumoObligatorioModel)
            .where(ConsumoObligatorioModel.Repuesto == repuesto)
        ).all()

        return [ConsumoObligatorioMapper.to_entity(m) for m in models]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(ConsumoObligatorioModel, _id)
        if row:
            self.session.delete(row)