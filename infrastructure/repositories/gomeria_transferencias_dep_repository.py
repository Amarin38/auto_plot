from typing import List

from sqlalchemy import select

from domain.entities.gomeria_transferencias_dep import GomeriaTransferenciasEntreDep
from infrastructure import SessionDB, db_engine
from infrastructure.db.models.gomeria_transferencias_dep_model import GomeriaTransferenciasEntreDepModel
from infrastructure.mappers.gomeria_transferencias_dep_mapper import GomeriaTransferenciasEntreDepMapper
from interfaces.repository import Repository


class GomeriaTransferenciasEntreDepRepository(Repository):
    def __init__(self) -> None:
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[GomeriaTransferenciasEntreDep]) -> None:
        with self.session as session:
            for e in entities:
                model = GomeriaTransferenciasEntreDepMapper.to_model(e)
                session.add(model)
                session.commit()


    # Read -------------------------------------------
    def get_all(self) -> List[GomeriaTransferenciasEntreDep]:
        with self.session as session:
            models = session.scalars(
                select(GomeriaTransferenciasEntreDepModel)
            ).all()

            return [GomeriaTransferenciasEntreDepMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> GomeriaTransferenciasEntreDep:
        with self.session as session:
            model = session.scalars(
                select(GomeriaTransferenciasEntreDepModel)
            ).filter(
                GomeriaTransferenciasEntreDepModel.id == _id
            ).first()

            return GomeriaTransferenciasEntreDepMapper.to_entity(model)


    def get_by_cabecera(self, cabecera: str) -> List[GomeriaTransferenciasEntreDep]:
        with self.session as session:
            model = session.scalars(
                select(GomeriaTransferenciasEntreDepModel)
                .where(GomeriaTransferenciasEntreDepModel.Cabecera == cabecera)
            ).all()

            return [GomeriaTransferenciasEntreDepMapper.to_entity(m) for m in model]

    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(GomeriaTransferenciasEntreDepModel, _id)
                if row:
                    session.delete(row)
