from domain.entities.consumo_historial import ConsumoHistorial
from infrastructure.db.models.consumo_historial_model import ConsumoHistorialModel


class ConsumoHistorialMapper:
    @staticmethod
    def to_entity(model: ConsumoHistorialModel) -> ConsumoHistorial:
        return ConsumoHistorial(
            id              = model.id,
            TipoRepuesto    = model.TipoRepuesto,
            Año             = model.Año,
            TotalConsumo    = model.TotalConsumo,
            FechaMin        = model.FechaMin,
            FechaMax        = model.FechaMax
        )

    @staticmethod
    def to_model(entity: ConsumoHistorial) -> ConsumoHistorialModel:
        return ConsumoHistorialModel(
            id              = entity.id,
            TipoRepuesto    = entity.TipoRepuesto,
            Año             = entity.Año,
            TotalConsumo    = entity.TotalConsumo,
            FechaMin        = entity.FechaMin,
            FechaMax        = entity.FechaMax
        )