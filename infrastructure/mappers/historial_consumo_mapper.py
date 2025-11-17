from domain.entities.historial_consumo import HistorialConsumo
from infrastructure.db.models.historial_consumo_model import HistorialConsumoModel


class HistorialConsumoMapper:
    @staticmethod
    def to_entity(model: HistorialConsumoModel) -> HistorialConsumo:
        return HistorialConsumo(
            id              = model.id,
            TipoRepuesto    = model.TipoRepuesto,
            Año             = model.Año,
            TotalConsumo    = model.TotalConsumo,
            FechaMin        = model.FechaMin,
            FechaMax        = model.FechaMax
        )

    @staticmethod
    def to_model(entity: HistorialConsumo) -> HistorialConsumoModel:
        return HistorialConsumoModel(
            id              = entity.id,
            TipoRepuesto    = entity.TipoRepuesto,
            Año             = entity.Año,
            TotalConsumo    = entity.TotalConsumo,
            FechaMin        = entity.FechaMin,
            FechaMax        = entity.FechaMax
        )