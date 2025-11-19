from typing import List

from sqlalchemy import select

from domain.entities.garantias_falla import GarantiasFalla
from infrastructure import SessionDB
from infrastructure import db_engine
from infrastructure.db.models.garantias_falla_model import GarantiasFallaModel
from infrastructure.mappers.garantias_falla_mapper import GarantiasFallaMapper

class GarantiasFallaRepository:
    def __init__(self) -> None:
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[GarantiasFalla]) -> None:
        with self.session as session:
            for e in entities:
                model = GarantiasFallaMapper.to_model(e)
                session.add(model)
                session.commit()


    # Read -------------------------------------------
    def get_all(self) -> List[GarantiasFalla]:
        with self.session as session:
            models = session.scalars(
                select(GarantiasFallaModel)
            ).all()

            return [GarantiasFallaMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> GarantiasFalla:
        with self.session as session:
            model = session.scalars(
                select(GarantiasFallaModel)
            ).filter(
                GarantiasFallaModel.id == _id
            ).first()

            return GarantiasFallaMapper.to_entity(model)


    def get_by_tipo_rep_and_cabecera(self, tipo_repuesto: str, cabecera: str) -> List[GarantiasFalla]:
        with self.session as session:
            models = session.scalars(
                select(GarantiasFallaModel)
                .where(GarantiasFallaModel.TipoRepuesto == tipo_repuesto,
                       GarantiasFallaModel.Cabecera == cabecera)
            ).all()

        return [GarantiasFallaMapper.to_entity(m) for m in models]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(GarantiasFallaModel, _id)
                if row:
                    session.delete(row)

