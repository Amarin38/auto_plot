from typing import List

from sqlalchemy import select

from domain.entities.indice_consumo import IndiceConsumo
from infrastructure import SessionDB, db_engine
from infrastructure.db.models.indice_consumo_model import IndiceConsumoModel
from infrastructure.mappers.indice_consumo_mapper import IndiceConsumoMapper
from interfaces.repository import Repository


class IndiceConsumoRepository(Repository):
    def __init__(self):
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[IndiceConsumo]) -> None:
        with self.session as session:
            for e in entities:
                model = IndiceConsumoMapper.to_model(e)
                session.add(model)
                session.commit()


    # Read -------------------------------------------
    def get_all(self) -> List[IndiceConsumo]:
        with self.session as session:
            models = session.scalars(
                select(IndiceConsumoModel)
            ).all()

            return [IndiceConsumoMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> IndiceConsumo:
        with self.session as session:
            model = session.scalars(
                select(IndiceConsumoModel)
            ).filter(
                IndiceConsumoModel.id == _id
            ).first()

            return IndiceConsumoMapper.to_entity(model)


    def get_by_tipo_rep_and_tipo_indice(self, tipo_repuesto, tipo_indice) -> List[IndiceConsumo]:
        with self.session as session:
            model = session.scalars(
                select(IndiceConsumoModel)
                .where(IndiceConsumoModel.TipoRepuesto == tipo_repuesto,
                                    IndiceConsumoModel.TipoOperacion == tipo_indice,
                                    )
            )

            return [IndiceConsumoMapper.to_entity(m) for m in model]

    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(IndiceConsumoModel, _id)
                if row:
                    session.delete(row)