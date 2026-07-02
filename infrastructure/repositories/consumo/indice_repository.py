from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select

from domain.entities.consumo.indice import ConsumoIndice
from infrastructure.db.models.consumo.indice_model import ConsumoIndiceModel
from infrastructure.mapper import Mapper


class ConsumoIndiceRepository:
    def __init__(self, session: Session):
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConsumoIndice]) -> None:
        models = [Mapper.to_model(entity, ConsumoIndiceModel) for entity in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[ConsumoIndice]:
        models = self.session.scalars(
            select(ConsumoIndiceModel)
        ).all()

        return [Mapper.to_entity(model, ConsumoIndice) for model in models]


    def get_by_id(self, _id: int) -> ConsumoIndice:
        model = self.session.scalars(
            select(ConsumoIndiceModel).where(ConsumoIndiceModel.id == _id)
        ).first()

        return Mapper.to_entity(model, ConsumoIndice)


    def get_by_tipo_rep_and_tipo_indice(self, tipo_repuesto, tipo_indice) -> List[ConsumoIndice]:
        models = self.session.scalars(
            select(ConsumoIndiceModel)
            .where(ConsumoIndiceModel.TipoRepuesto == tipo_repuesto,
                   ConsumoIndiceModel.TipoOperacion == tipo_indice)
        ).all()

        return [Mapper.to_entity(model, ConsumoIndice) for model in models]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(ConsumoIndiceModel, _id)
        if row:
            self.session.delete(row)
