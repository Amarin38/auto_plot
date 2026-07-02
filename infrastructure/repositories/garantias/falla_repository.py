from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.garantias.falla import GarantiasFalla
from infrastructure.db.models.garantias.falla_model import GarantiasFallaModel
from infrastructure.mapper import Mapper


class GarantiasFallaRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[GarantiasFalla]) -> None:
        models = [Mapper.to_model(entity, GarantiasFallaModel) for entity in entities]
        self.session.add_all(models)

    # Read -------------------------------------------
    def get_all(self) -> List[GarantiasFalla]:
        models = self.session.scalars(
            select(GarantiasFallaModel)
        ).all()

        return [Mapper.to_entity(model, GarantiasFalla) for model in models]


    def get_by_id(self, _id: int) -> GarantiasFalla:
        model = self.session.scalars(
            select(GarantiasFallaModel).where(GarantiasFallaModel.id == _id)
        ).first()

        return Mapper.to_entity(model, GarantiasFalla)


    def get_by_tipo_rep_and_cabecera(self, tipo_repuesto: str, cabecera: str) -> List[GarantiasFalla]:
        models = self.session.scalars(
            select(GarantiasFallaModel)
            .where(GarantiasFallaModel.TipoRepuesto == tipo_repuesto,
                   GarantiasFallaModel.Cabecera == cabecera)
        ).all()

        return [Mapper.to_entity(model, GarantiasFalla) for model in models]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(GarantiasFallaModel, _id)
        if row:
            self.session.delete(row)

