from typing import List

from sqlalchemy import select

from domain.entities.services.falla_garantias import FallaGarantias
from infrastructure import SessionDB
from infrastructure import db_engine
from infrastructure.db.models.services.falla_garantias_model import FallaGarantiasModel
from infrastructure.mappers.services.falla_garantias_mapper import FallaGarantiasMapper

class FallaGarantiasRepository:
    def __init__(self) -> None:
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[FallaGarantias]) -> None:
        with self.session as session:
            for e in entities:
                model = FallaGarantiasMapper.to_model(e)
                session.add(model)
                session.commit()


    # Read -------------------------------------------
    def get_all(self) -> List[FallaGarantias]:
        with self.session as session:
            models = session.scalars(
                select(FallaGarantiasModel)
            ).all()

            return [FallaGarantiasMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> FallaGarantias:
        with self.session as session:
            model = session.scalars(
                select(FallaGarantiasModel)
            ).filter(
                FallaGarantiasModel.id == _id
            ).first()

            return FallaGarantiasMapper.to_entity(model)


    def get_by_tipo_rep_and_cabecera(self, tipo_repuesto: str, cabecera: str) -> List[FallaGarantias]:
        with self.session as session:
            models = session.scalars(
                select(FallaGarantiasModel)
                .where(FallaGarantiasModel.TipoRepuesto == tipo_repuesto,
                       FallaGarantiasModel.Cabecera == cabecera)
            ).all()

        return [FallaGarantiasMapper.to_entity(m) for m in models]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(FallaGarantiasModel, _id)
                if row:
                    session.delete(row)

