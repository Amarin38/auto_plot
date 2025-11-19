from typing import List

from sqlalchemy import select

from domain.entities.consumo_indice import ConsumoIndice
from infrastructure import SessionDB, db_engine
from infrastructure.db.models.consumo_indice_model import ConsumoIndiceModel
from infrastructure.mappers.consumo_indice_mapper import ConsumoIndiceMapper
from interfaces.repository import Repository


class ConsumoIndiceRepository(Repository):
    def __init__(self):
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConsumoIndice]) -> None:
        with self.session as session:
            for e in entities:
                model = ConsumoIndiceMapper.to_model(e)
                session.add(model)
                session.commit()


    # Read -------------------------------------------
    def get_all(self) -> List[ConsumoIndice]:
        with self.session as session:
            models = session.scalars(
                select(ConsumoIndiceModel)
            ).all()

            return [ConsumoIndiceMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> ConsumoIndice:
        with self.session as session:
            model = session.scalars(
                select(ConsumoIndiceModel)
            ).filter(
                ConsumoIndiceModel.id == _id
            ).first()

            return ConsumoIndiceMapper.to_entity(model)


    def get_by_tipo_rep_and_tipo_indice(self, tipo_repuesto, tipo_indice) -> List[ConsumoIndice]:
        with self.session as session:
            model = session.scalars(
                select(ConsumoIndiceModel)
                .where(ConsumoIndiceModel.TipoRepuesto == tipo_repuesto,
                       ConsumoIndiceModel.TipoOperacion == tipo_indice,
                       )
            )

            return [ConsumoIndiceMapper.to_entity(m) for m in model]

    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(ConsumoIndiceModel, _id)
                if row:
                    session.delete(row)