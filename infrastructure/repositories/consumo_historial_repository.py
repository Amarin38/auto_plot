from typing import List

from sqlalchemy import select

from config.enums import RepuestoEnum
from domain.entities.consumo_historial import ConsumoHistorial
from infrastructure import SessionDB, db_engine
from infrastructure.db.models.consumo_historial_model import ConsumoHistorialModel
from infrastructure.mappers.consumo_historial_mapper import ConsumoHistorialMapper
from interfaces.repository import Repository


class ConsumoHistorialRepository(Repository):
    def __init__(self):
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConsumoHistorial]) -> None:
        with self.session as session:
            for e in entities:
                model = ConsumoHistorialMapper.to_model(e)
                session.add(model)
                session.commit()


    # Read -------------------------------------------
    def get_all(self) -> List[ConsumoHistorial]:
        with self.session as session:
            models = session.scalars(
                select(ConsumoHistorialModel)
            ).all()

            return [ConsumoHistorialMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> ConsumoHistorial:
        with self.session as session:
            model = session.scalars(
                select(ConsumoHistorialModel)
            ).filter(
                ConsumoHistorialModel.id == _id
            ).first()

            return ConsumoHistorialMapper.to_entity(model)


    def get_by_tipo_rep(self, tipo_repuesto: RepuestoEnum) -> List[ConsumoHistorial]:
        with self.session as session:
            model = session.scalars(
                select(ConsumoHistorialModel)
                .where(ConsumoHistorialModel.TipoRepuesto == tipo_repuesto)
            )

            return [ConsumoHistorialMapper.to_entity(m) for m in model]

    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(ConsumoHistorialModel, _id)
                if row:
                    session.delete(row)