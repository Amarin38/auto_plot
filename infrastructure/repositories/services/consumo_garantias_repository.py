from typing import List

from sqlalchemy import select

from domain.entities.services.consumo_garantias import ConsumoGarantias
from infrastructure import SessionServices
from infrastructure import services_engine
from infrastructure.db.models.services.consumo_garantias_model import ConsumoGarantiasModel
from infrastructure.mappers.services.consumo_garantias_mapper import ConsumoGarantiasMapper

class ConsumoGarantiasRepository:
    def __init__(self) -> None:
        self.session = SessionServices()
        self.engine = services_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConsumoGarantias]) -> None:
        with self.session as session:
            for e in entities:
                model = ConsumoGarantiasMapper.to_model(e)
                session.add(model)
                session.commit()


    # Read -------------------------------------------
    def get_all(self) -> List[ConsumoGarantias]:
        with self.session as session:
            models = session.scalars(
                select(ConsumoGarantiasModel)
            ).all()

            return [ConsumoGarantiasMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> ConsumoGarantias:
        with self.session as session:
            model = session.scalars(
                select(ConsumoGarantiasModel)
            ).filter(
                ConsumoGarantiasModel.id == _id
            ).first()

            return ConsumoGarantiasMapper.to_entity(model)


    def get_by_tipo_rep_and_cabecera(self, tipo_repuesto: str, cabecera: str) -> List[ConsumoGarantias]:
        with self.session as session:
            models = session.scalars(
                select(ConsumoGarantiasModel)
                .where(ConsumoGarantiasModel.TipoRepuesto == tipo_repuesto,
                       ConsumoGarantiasModel.Cabecera == cabecera)
            ).all()

            return [ConsumoGarantiasMapper.to_entity(m) for m in models]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(ConsumoGarantiasModel, _id)
                if row:
                    session.delete(row)
