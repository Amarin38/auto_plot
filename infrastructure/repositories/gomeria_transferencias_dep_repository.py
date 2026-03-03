from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.gomeria_transferencias_dep import GomeriaTransferenciasEntreDep
from infrastructure.db.models.gomeria_transferencias_dep_model import GomeriaTransferenciasEntreDepModel
from infrastructure.mappers.gomeria_transferencias_dep_mapper import GomeriaTransferenciasEntreDepMapper
from interfaces.repository import Repository


class GomeriaTransferenciasEntreDepRepository(Repository):
    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[GomeriaTransferenciasEntreDep]) -> None:
        models = [GomeriaTransferenciasEntreDepMapper.to_model(e) for e in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[GomeriaTransferenciasEntreDep]:
        models = self.session.scalars(
            select(GomeriaTransferenciasEntreDepModel)
        ).all()

        return [GomeriaTransferenciasEntreDepMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> GomeriaTransferenciasEntreDep:
        model = self.session.scalars(
            select(GomeriaTransferenciasEntreDepModel)
            .where(GomeriaTransferenciasEntreDepModel.id == _id)
        ).first()

        return GomeriaTransferenciasEntreDepMapper.to_entity(model)


    def get_by_cabecera(self, cabecera: str) -> List[GomeriaTransferenciasEntreDep]:
        model = self.session.scalars(
            select(GomeriaTransferenciasEntreDepModel)
            .where(GomeriaTransferenciasEntreDepModel.Cabecera == cabecera)
        ).all()

        return [GomeriaTransferenciasEntreDepMapper.to_entity(m) for m in model]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(GomeriaTransferenciasEntreDepModel, _id)
        if row:
            self.session.delete(row)
