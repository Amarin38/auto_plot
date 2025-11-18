from typing import List

from sqlalchemy import select

from config.enums import CabecerasEnum, ConsumoObligatorioEnum
from domain.entities.consumo_obligatorio import ConsumoObligatorio
from infrastructure import SessionDB, db_engine
from infrastructure.db.models.consumo_obligatorio_model import ConsumoObligatorioModel
from infrastructure.mappers.consumo_obligatorio_mapper import ConsumoObligatorioMapper
from interfaces.repository import Repository


class ConsumoObligatorioRepository(Repository):
    def __init__(self):
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConsumoObligatorio]) -> None:
        with self.session as session:
            for e in entities:
                model = ConsumoObligatorioMapper.to_model(e)
                session.add(model)
                session.commit()

    # Read -------------------------------------------
    def get_all(self) -> List[ConsumoObligatorio]:
        with self.session as session:
            models = session.scalars(
                select(ConsumoObligatorioModel)
            ).all()

            return [ConsumoObligatorioMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> ConsumoObligatorio:
        with self.session as session:
            model = session.scalars(
                select(ConsumoObligatorioModel)
            ).filter(
                ConsumoObligatorioModel.id == _id
            ).first()

            return ConsumoObligatorioMapper.to_entity(model)


    def get_by_repuesto(self, repuesto: ConsumoObligatorioEnum) -> List[ConsumoObligatorio]:
        with self.session as session:
            models = session.scalars(
                select(ConsumoObligatorioModel)
                .where(ConsumoObligatorioModel.Repuesto == repuesto)
            ).all()

            return [ConsumoObligatorioMapper.to_entity(m) for m in models]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(ConsumoObligatorioModel, _id)
                if row:
                    session.delete(row)