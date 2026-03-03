from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.coches_cabecera import CochesCabecera
from infrastructure.db.models.coches_cabecera_model import CochesCabeceraModel
from infrastructure.mappers.coches_cabecera_mapper import CochesCabeceraMapper
from interfaces.repository import Repository


class CochesCabeceraRepository(Repository):
    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[CochesCabecera]) -> None:
        models = [CochesCabeceraMapper.to_model(e) for e in entities]
        self.session.add_all(models)

    # Read -------------------------------------------
    def get_all(self) -> List[CochesCabecera]:
        models = self.session.scalars(
            select(CochesCabeceraModel)
        ).all()

        return [CochesCabeceraMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> CochesCabecera:
        model = self.session.scalars(
            select(CochesCabeceraModel).where(CochesCabeceraModel.id == _id)
        ).first()

        return CochesCabeceraMapper.to_entity(model)


    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(CochesCabeceraModel, _id)
        if row:
            self.session.delete(row)