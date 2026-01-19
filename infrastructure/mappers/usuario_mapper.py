from domain.entities.usuario import Usuario
from infrastructure.db.models.usuario_model import UsuarioModel
from interfaces.mapper import Mapper


class UsuarioMapper(Mapper):
    @staticmethod
    def to_entity(model: UsuarioModel) -> Usuario:
        return Usuario(
            Nombre      = model.Nombre,
            Contraseña  = model.Contraseña,
            Rol         = model.Rol,
        )

    @staticmethod
    def to_model(entity: Usuario) -> UsuarioModel:
        return UsuarioModel(
            Nombre      = entity.Nombre,
            Contraseña  = entity.Contraseña,
            Rol         = entity.Rol,
        )