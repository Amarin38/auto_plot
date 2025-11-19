from domain.entities.garantias_falla import GarantiasFalla
from infrastructure.db.models.garantias_falla_model import GarantiasFallaModel

class GarantiasFallaMapper:
    @staticmethod
    def to_entity(model: GarantiasFallaModel) -> GarantiasFalla:
        return GarantiasFalla(
            id                          = model.id,
            Cabecera                    = model.Cabecera,
            Repuesto                    = model.Repuesto,
            TipoRepuesto                = model.TipoRepuesto,
            PromedioTiempoFalla         = model.PromedioTiempoFalla,
        )

    @staticmethod
    def to_model(entity: GarantiasFalla) -> GarantiasFallaModel:
        return GarantiasFallaModel(
            id                          = entity.id,
            Cabecera                    = entity.Cabecera,
            Repuesto                    = entity.Repuesto,
            TipoRepuesto                = entity.TipoRepuesto,
            PromedioTiempoFalla         = entity.PromedioTiempoFalla,
        )