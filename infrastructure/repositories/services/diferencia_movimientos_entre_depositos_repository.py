from typing import List

from sqlalchemy import select

from domain.entities.services.diferencia_movimientos_entre_depositos import DiferenciaMovimientosEntreDepositos
from infrastructure import db_engine, SessionDB
from infrastructure.db.models.services.diferencia_movimientos_entre_depositos_model import \
    DiferenciaMovimientosEntreDepositosModel
from infrastructure.mappers.services.diferencia_movimientos_entre_depositos_mapper import \
    DiferenciaMovimientosEntreDepositosMapper
from interfaces.repository import Repository


class DiferenciaMovimientosEntreDepositosRepository(Repository):
    def __init__(self) -> None:
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[DiferenciaMovimientosEntreDepositos]) -> None:
        with self.session as session:
            for e in entities:
                model = DiferenciaMovimientosEntreDepositosMapper.to_model(e)
                session.add(model)
                session.commit()


    # Read -------------------------------------------
    def get_all(self) -> List[DiferenciaMovimientosEntreDepositos]:
        with self.session as session:
            models = session.scalars(
                select(DiferenciaMovimientosEntreDepositosModel)
            ).all()

            return [DiferenciaMovimientosEntreDepositosMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> DiferenciaMovimientosEntreDepositos:
        with self.session as session:
            model = session.scalars(
                select(DiferenciaMovimientosEntreDepositosModel)
            ).filter(
                DiferenciaMovimientosEntreDepositosModel.id == _id
            ).first()

            return DiferenciaMovimientosEntreDepositosMapper.to_entity(model)


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(DiferenciaMovimientosEntreDepositosModel, _id)
                if row:
                    session.delete(row)