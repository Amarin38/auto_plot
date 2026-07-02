from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.gomeria.transferencias_dep import GomeriaTransferenciasEntreDep
from infrastructure.db.models.gomeria.transferencias_dep_model import GomeriaTransferenciasEntreDepModel
from infrastructure.mapper import Mapper


class GomeriaTransferenciasEntreDepRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[GomeriaTransferenciasEntreDep]) -> None:
        models = [Mapper.to_model(entity, GomeriaTransferenciasEntreDepModel) for entity in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[GomeriaTransferenciasEntreDep]:
        models = self.session.scalars(
            select(GomeriaTransferenciasEntreDepModel)
        ).all()

        return [Mapper.to_entity(model, GomeriaTransferenciasEntreDep) for model in models]


    def get_by_id(self, _id: int) -> GomeriaTransferenciasEntreDep:
        model = self.session.scalars(
            select(GomeriaTransferenciasEntreDepModel)
            .where(GomeriaTransferenciasEntreDepModel.id == _id)
        ).first()

        return Mapper.to_entity(model, GomeriaTransferenciasEntreDep)


    def get_by_cabecera(self, cabecera: str) -> List[GomeriaTransferenciasEntreDep]:
        models = self.session.scalars(
            select(GomeriaTransferenciasEntreDepModel)
            .where(GomeriaTransferenciasEntreDepModel.Cabecera == cabecera)
        ).all()

        return [Mapper.to_entity(model, GomeriaTransferenciasEntreDep) for model in models]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(GomeriaTransferenciasEntreDepModel, _id)
        if row:
            self.session.delete(row)
