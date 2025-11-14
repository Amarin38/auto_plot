from typing import List

from sqlalchemy import select

from domain.entities.transferencias_entre_dep import TransferenciasEntreDepositos
from infrastructure import SessionDB, db_engine
from infrastructure.db.models.transferencias_entre_dep_model import TransferenciasEntreDepositosModel
from infrastructure.mappers.transferencias_dep_mapper import TransferenciasEntreDepositosMapper
from interfaces.repository import Repository


class TransferenciasEntreDepositosRepository(Repository):
    def __init__(self) -> None:
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[TransferenciasEntreDepositos]) -> None:
        with self.session as session:
            for e in entities:
                model = TransferenciasEntreDepositosMapper.to_model(e)
                session.add(model)
                session.commit()


    # Read -------------------------------------------
    def get_all(self) -> List[TransferenciasEntreDepositos]:
        with self.session as session:
            models = session.scalars(
                select(TransferenciasEntreDepositosModel)
            ).all()

            return [TransferenciasEntreDepositosMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> TransferenciasEntreDepositos:
        with self.session as session:
            model = session.scalars(
                select(TransferenciasEntreDepositosModel)
            ).filter(
                TransferenciasEntreDepositosModel.id == _id
            ).first()

            return TransferenciasEntreDepositosMapper.to_entity(model)


    def get_by_cabecera(self, cabecera: str) -> List[TransferenciasEntreDepositos]:
        with self.session as session:
            model = session.scalars(
                select(TransferenciasEntreDepositosModel)
                .where(TransferenciasEntreDepositosModel.Cabecera == cabecera)
            ).all()

            return [TransferenciasEntreDepositosMapper.to_entity(m) for m in model]

    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(TransferenciasEntreDepositosModel, _id)
                if row:
                    session.delete(row)
