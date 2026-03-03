from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.usuario import Usuario
from infrastructure.db.models.usuario_model import UsuarioModel
from infrastructure.mappers.usuario_mapper import UsuarioMapper


class UsuarioRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[Usuario]) -> None:
        models = [UsuarioMapper.to_model(e) for e in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[Usuario]:
        models = self.session.scalars(
            select(UsuarioModel)
        ).all()

        return [UsuarioMapper.to_entity(m) for m in models]


    def get_by_nombre(self, nombre: str) -> Usuario:
        model = self.session.scalars(
            select(UsuarioModel).where(UsuarioModel.Nombre == nombre)
        ).first()

        return UsuarioMapper.to_entity(model)


    # Delete -------------------------------------------
    def delete_by_id(self, nombre: str) -> None:
            row = self.session.get(UsuarioModel, nombre)
            if row:
                self.session.delete(row)

