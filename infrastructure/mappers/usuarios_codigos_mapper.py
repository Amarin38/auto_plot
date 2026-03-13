from domain.entities.usuarios_codigos import UsuariosCodigos
from infrastructure.db.models.usuarios_codigos_model import UsuariosCodigosModel


class UsuariosCodigosMapper:
    @staticmethod
    def to_entity(model: UsuariosCodigosModel) -> UsuariosCodigos:
        return UsuariosCodigos(
            id                  = model.id,
            UsuariosAntiguos    = model.UsuariosAntiguos,
            UsuariosNuevos      = model.UsuariosNuevos,
            NombresAntiguos     = model.NombresAntiguos,
            NombresNuevos       = model.NombresNuevos,
        )

    @staticmethod
    def to_model(entity: UsuariosCodigos) -> UsuariosCodigosModel:
        return UsuariosCodigosModel(
            id                  = entity.id,
            UsuariosAntiguos    = entity.UsuariosAntiguos,
            UsuariosNuevos      = entity.UsuariosNuevos,
            NombresAntiguos     = entity.NombresAntiguos,
            NombresNuevos       = entity.NombresNuevos,
        )