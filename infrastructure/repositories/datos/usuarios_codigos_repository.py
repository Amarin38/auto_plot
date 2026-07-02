from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select

from domain.entities.datos.usuarios_codigos import UsuariosCodigos
from infrastructure.db.models.datos.usuarios_codigos_model import UsuariosCodigosModel
from infrastructure.mapper import Mapper


class UsuariosCodigosRepository:
    def __init__(self, session: Session):
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[UsuariosCodigos]) -> None:
        models = [Mapper.to_model(entity, UsuariosCodigosModel) for entity in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[UsuariosCodigos]:
        models = self.session.scalars(
            select(UsuariosCodigosModel)
        ).all()

        return [Mapper.to_entity(model, UsuariosCodigos) for model in models]


    def get_by_id(self, _id: int) -> UsuariosCodigos:
        model = self.session.scalars(
            select(UsuariosCodigosModel).where(UsuariosCodigosModel.id == _id)
        ).first()

        return Mapper.to_entity(model, UsuariosCodigos)


    def get_by_usuario_antiguo(self, usuario_antiguo: str) -> List[UsuariosCodigos]:
        models = self.session.scalars(
            select(UsuariosCodigosModel)
            .where(UsuariosCodigosModel.UsuariosAntiguos == usuario_antiguo)
        ).all()

        return [Mapper.to_entity(model, UsuariosCodigos) for model in models]


    def get_by_usuario_nuevo(self, usuario_nuevo: str) -> List[UsuariosCodigos]:
        models = self.session.scalars(
            select(UsuariosCodigosModel)
            .where(UsuariosCodigosModel.UsuariosNuevos == usuario_nuevo)
        ).all()

        return [Mapper.to_entity(model, UsuariosCodigos) for model in models]

    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(UsuariosCodigosModel, _id)
        if row:
            self.session.delete(row)
