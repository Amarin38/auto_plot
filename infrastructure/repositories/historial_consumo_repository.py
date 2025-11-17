from typing import List

from sqlalchemy import select

from config.enums import RepuestoEnum
from domain.entities.historial_consumo import HistorialConsumo
from infrastructure import SessionDB, db_engine
from infrastructure.db.models.historial_consumo_model import HistorialConsumoModel
from infrastructure.mappers.historial_consumo_mapper import HistorialConsumoMapper
from interfaces.repository import Repository


class HistorialConsumoRepository(Repository):
    def __init__(self):
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[HistorialConsumo]) -> None:
        with self.session as session:
            for e in entities:
                model = HistorialConsumoMapper.to_model(e)
                session.add(model)
                session.commit()


    # Read -------------------------------------------
    def get_all(self) -> List[HistorialConsumo]:
        with self.session as session:
            models = session.scalars(
                select(HistorialConsumoModel)
            ).all()

            return [HistorialConsumoMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> HistorialConsumo:
        with self.session as session:
            model = session.scalars(
                select(HistorialConsumoModel)
            ).filter(
                HistorialConsumoModel.id == _id
            ).first()

            return HistorialConsumoMapper.to_entity(model)


    def get_by_tipo_rep(self, tipo_repuesto: RepuestoEnum) -> List[HistorialConsumo]:
        with self.session as session:
            model = session.scalars(
                select(HistorialConsumoModel)
                .where(HistorialConsumoModel.TipoRepuesto == tipo_repuesto)
            )

            return [HistorialConsumoMapper.to_entity(m) for m in model]

    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(HistorialConsumoModel, _id)
                if row:
                    session.delete(row)