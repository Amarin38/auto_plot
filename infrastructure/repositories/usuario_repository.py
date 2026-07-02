from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.usuario import Usuario
from infrastructure.db.models.usuario_model import UsuarioModel
from infrastructure.mapper import Mapper


class UsuarioRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[Usuario]) -> None:
        models = [Mapper.to_model(entity, UsuarioModel) for entity in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[Usuario]:
        models = self.session.scalars(
            select(UsuarioModel)
        ).all()

        return [Mapper.to_entity(model, Usuario) for model in models]


    def get_by_nombre(self, nombre: str) -> Usuario:
        model = self.session.scalars(
            select(UsuarioModel).where(UsuarioModel.Nombre == nombre)
        ).first()

        return Mapper.to_entity(model, Usuario)


    # Delete -------------------------------------------
    def delete_by_id(self, nombre: str) -> None:
            row = self.session.get(UsuarioModel, nombre)
            if row:
                self.session.delete(row)

