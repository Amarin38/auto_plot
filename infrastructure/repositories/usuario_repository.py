from typing import List

from sqlalchemy import select

from domain.entities.usuario import Usuario
from infrastructure import SessionDB, db_engine
from infrastructure.db.models.usuario_model import UsuarioModel
from infrastructure.mappers.usuario_mapper import UsuarioMapper


class UsuarioRepository:
    def __init__(self) -> None:
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, user: Usuario) -> None:
        with self.session as session:
            model = UsuarioMapper.to_model(user)
            session.add(model)
            session.commit()

    # Read -------------------------------------------
    def get_all(self) -> List[Usuario]:
        with self.session as session:
            models = session.scalars(
                select(UsuarioModel)
            ).all()

            return [UsuarioMapper.to_entity(m) for m in models]


    def get_by_nombre(self, nombre: str) -> Usuario:
        with self.session as session:
            model = session.scalars(
                select(UsuarioModel)
                .where(UsuarioModel.Nombre == nombre)
            ).first()

            return UsuarioMapper.to_entity(model)


    # Delete -------------------------------------------
    def delete_by_id(self, nombre: str) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(UsuarioModel, nombre)
                if row:
                    session.delete(row)

