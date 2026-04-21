from domain.entities.datos_repuestos_codigos import RepuestosCodigos
from infrastructure.db.models.datos_repuestos_codigos_model import RepuestosCodigosModel


class RepuestosCodigosMapper:
    @staticmethod
    def to_entity(model: RepuestosCodigosModel) -> RepuestosCodigos:
        return RepuestosCodigos(
            id              = model.id,
            Descripcion     = model.Descripcion,
            Deposito        = model.Deposito,
            Familia         = model.Familia,
            Articulo        = model.Articulo,
            Codigos         = model.Codigos,
            CodigosConCero  = model.CodigosConCero
        )

    @staticmethod
    def to_model(entity: RepuestosCodigos) -> RepuestosCodigosModel:
        return RepuestosCodigosModel(
            id              = entity.id,
            Descripcion     = entity.Descripcion,
            Deposito        = entity.Deposito,
            Familia         = entity.Familia,
            Articulo        = entity.Articulo,
            Codigos         = entity.Codigos,
            CodigosConCero  = entity.CodigosConCero
        )