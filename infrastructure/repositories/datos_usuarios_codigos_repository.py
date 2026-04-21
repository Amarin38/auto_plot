from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select

from domain.entities.datos_usuarios_codigos import UsuariosCodigos
from infrastructure.db.models.datos_usuarios_codigos_model import UsuariosCodigosModel
from infrastructure.mappers.datos_usuarios_codigos_mapper import UsuariosCodigosMapper
from interfaces.repository import Repository


class UsuariosCodigosRepository(Repository):
    def __init__(self, session: Session):
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[UsuariosCodigos]) -> None:
        models = [UsuariosCodigosMapper.to_model(e) for e in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[UsuariosCodigos]:
        models = self.session.scalars(
            select(UsuariosCodigosModel)
        ).all()

        return [UsuariosCodigosMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> UsuariosCodigos:
        model = self.session.scalars(
            select(UsuariosCodigosModel).where(UsuariosCodigosModel.id == _id)
        ).first()

        return UsuariosCodigosMapper.to_entity(model)


    def get_by_usuario_antiguo(self, usuario_antiguo: str) -> List[UsuariosCodigos]:
        model = self.session.scalars(
            select(UsuariosCodigosModel)
            .where(UsuariosCodigosModel.UsuariosAntiguos == usuario_antiguo)
        ).all()

        return [UsuariosCodigosMapper.to_entity(m) for m in model]


    def get_by_usuario_nuevo(self, usuario_nuevo: str) -> List[UsuariosCodigos]:
        model = self.session.scalars(
            select(UsuariosCodigosModel)
            .where(UsuariosCodigosModel.UsuariosNuevos == usuario_nuevo)
        ).all()

        return [UsuariosCodigosMapper.to_entity(m) for m in model]

    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(UsuariosCodigosModel, _id)
        if row:
            self.session.delete(row)
