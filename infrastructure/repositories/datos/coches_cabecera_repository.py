from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.datos.coches_cabecera import CochesCabecera
from infrastructure.db.models.datos.coches_cabecera_model import CochesCabeceraModel
from infrastructure.mapper import Mapper


class CochesCabeceraRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[CochesCabecera]) -> None:
        models = [Mapper.to_model(entity, CochesCabeceraModel) for entity in entities]
        self.session.add_all(models)

    # Read -------------------------------------------
    def get_all(self) -> List[CochesCabecera]:
        models = self.session.scalars(
            select(CochesCabeceraModel)
        ).all()

        return [Mapper.to_entity(model, CochesCabecera) for model in models]


    def get_by_id(self, _id: int) -> CochesCabecera:
        model = self.session.scalars(
            select(CochesCabeceraModel).where(CochesCabeceraModel.id == _id)
        ).first()

        return Mapper.to_entity(model, CochesCabecera)


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(CochesCabeceraModel, _id)
        if row:
            self.session.delete(row)