from typing import List

from sqlalchemy import select

from domain.entities.garantias_consumo import GarantiasConsumo
from infrastructure import SessionDB, db_engine
from infrastructure.db.models.garantias_consumo_model import GarantiasConsumoModel
from infrastructure.mappers.garantias_consumo_mapper import GarantiasConsumoMapper

class GarantiasConsumoRepository:
    def __init__(self) -> None:
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[GarantiasConsumo]) -> None:
        with self.session as session:
            for e in entities:
                model = GarantiasConsumoMapper.to_model(e)
                session.add(model)
                session.commit()


    # Read -------------------------------------------
    def get_all(self) -> List[GarantiasConsumo]:
        with self.session as session:
            models = session.scalars(
                select(GarantiasConsumoModel)
            ).all()

            return [GarantiasConsumoMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> GarantiasConsumo:
        with self.session as session:
            model = session.scalars(
                select(GarantiasConsumoModel)
            ).filter(
                GarantiasConsumoModel.id == _id
            ).first()

            return GarantiasConsumoMapper.to_entity(model)


    def get_by_tipo_rep_and_cabecera(self, tipo_repuesto: str, cabecera: str) -> List[GarantiasConsumo]:
        with self.session as session:
            models = session.scalars(
                select(GarantiasConsumoModel)
                .where(GarantiasConsumoModel.TipoRepuesto == tipo_repuesto,
                       GarantiasConsumoModel.Cabecera == cabecera)
            ).all()

            return [GarantiasConsumoMapper.to_entity(m) for m in models]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(GarantiasConsumoModel, _id)
                if row:
                    session.delete(row)
