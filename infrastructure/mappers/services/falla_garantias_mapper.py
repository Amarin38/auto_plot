from domain.entities.services.falla_garantias import FallaGarantias
from infrastructure.db.models.services.falla_garantias_model import FallaGarantiasModel

class FallaGarantiasMapper:
    @staticmethod
    def to_entity(model: FallaGarantiasModel) -> FallaGarantias:
        return FallaGarantias(
            id                          = model.id,
            Cabecera                    = model.Cabecera,
            Repuesto                    = model.Repuesto,
            TipoRepuesto                = model.TipoRepuesto,
            PromedioTiempoFalla         = model.PromedioTiempoFalla,
        )

    @staticmethod
    def to_model(entity: FallaGarantias) -> FallaGarantiasModel:
        return FallaGarantiasModel(
            id                          = entity.id,
            Cabecera                    = entity.Cabecera,
            Repuesto                    = entity.Repuesto,
            TipoRepuesto                = entity.TipoRepuesto,
            PromedioTiempoFalla         = entity.PromedioTiempoFalla,
        )