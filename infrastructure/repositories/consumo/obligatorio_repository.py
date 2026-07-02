from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from config.enums import ConsumoObligatorioEnum
from domain.entities.consumo.obligatorio import ConsumoObligatorio
from infrastructure.db.models.consumo.obligatorio_model import ConsumoObligatorioModel
from infrastructure.mapper import Mapper


class ConsumoObligatorioRepository:
    def __init__(self, session: Session):
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConsumoObligatorio]) -> None:
        models = [Mapper.to_model(entity, ConsumoObligatorioModel) for entity in entities]
        self.session.add_all(models)

    # Read -------------------------------------------
    def get_all(self) -> List[ConsumoObligatorio]:
        models = self.session.scalars(
            select(ConsumoObligatorioModel)
        ).all()

        return [Mapper.to_entity(model, ConsumoObligatorio) for model in models]


    def get_by_id(self, _id: int) -> ConsumoObligatorio:
        model = self.session.scalars(
            select(ConsumoObligatorioModel).where(ConsumoObligatorioModel.id == _id)
        ).first()

        return Mapper.to_entity(model, ConsumoObligatorio)


    def get_by_repuesto(self, repuesto: ConsumoObligatorioEnum) -> List[ConsumoObligatorio]:
        models = self.session.scalars(
            select(ConsumoObligatorioModel)
            .where(ConsumoObligatorioModel.Repuesto == repuesto)
        ).all()

        return [Mapper.to_entity(model, ConsumoObligatorio) for model in models]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(ConsumoObligatorioModel, _id)
        if row:
            self.session.delete(row)