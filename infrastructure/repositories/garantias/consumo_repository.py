from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.garantias.consumo import GarantiasConsumo
from infrastructure.db.models.garantias.consumo_model import GarantiasConsumoModel
from infrastructure.mapper import Mapper


class GarantiasConsumoRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[GarantiasConsumo]) -> None:
        models = [Mapper.to_model(entity, GarantiasConsumoModel) for entity in entities]
        self.session.add_all(models)

    # Read -------------------------------------------
    def get_all(self) -> List[GarantiasConsumo]:
        models = self.session.scalars(
            select(GarantiasConsumoModel)
        ).all()

        return [Mapper.to_entity(model, GarantiasConsumo) for model in models]


    def get_by_id(self, _id: int) -> GarantiasConsumo:
        model = self.session.scalars(
            select(GarantiasConsumoModel).where(GarantiasConsumoModel.id == _id)
        ).first()

        return Mapper.to_entity(model, GarantiasConsumo)


    def get_by_tipo_rep_and_cabecera(self, tipo_repuesto: str, cabecera: str) -> List[GarantiasConsumo]:
        models = self.session.scalars(
            select(GarantiasConsumoModel)
            .where(GarantiasConsumoModel.TipoRepuesto == tipo_repuesto,
                   GarantiasConsumoModel.Cabecera == cabecera)
        ).all()

        return [Mapper.to_entity(model, GarantiasConsumo) for model in models]


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(GarantiasConsumoModel, _id)
        if row:
            self.session.delete(row)
