from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select

from domain.entities.consumo_indice import ConsumoIndice
from infrastructure.db.models.consumo_indice_model import ConsumoIndiceModel
from infrastructure.mappers.consumo_indice_mapper import ConsumoIndiceMapper
from interfaces.repository import Repository


class ConsumoIndiceRepository(Repository):
    def __init__(self, session: Session):
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConsumoIndice]) -> None:
        models = [ConsumoIndiceMapper.to_model(e) for e in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[ConsumoIndice]:
        models = self.session.scalars(
            select(ConsumoIndiceModel)
        ).all()

        return [ConsumoIndiceMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> ConsumoIndice:
        model = self.session.scalars(
            select(ConsumoIndiceModel).where(ConsumoIndiceModel.id == _id)
        ).first()

        return ConsumoIndiceMapper.to_entity(model)


    def get_by_tipo_rep_and_tipo_indice(self, tipo_repuesto, tipo_indice) -> List[ConsumoIndice]:
        model = self.session.scalars(
            select(ConsumoIndiceModel)
            .where(ConsumoIndiceModel.TipoRepuesto == tipo_repuesto,
                   ConsumoIndiceModel.TipoOperacion == tipo_indice)
        ).all()

        return [ConsumoIndiceMapper.to_entity(m) for m in model]

    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(ConsumoIndiceModel, _id)
        if row:
            self.session.delete(row)
