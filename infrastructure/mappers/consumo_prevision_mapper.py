from domain.entities.consumo_prevision import ConsumoPrevision
from infrastructure.db.models.consumo_prevision_model import ConsumoPrevisionModel


class ConsumoPrevisionMapper:
    @staticmethod
    def to_entity(model: ConsumoPrevisionModel) -> ConsumoPrevision:
        return ConsumoPrevision(
            id              = model.id,
            FechaCompleta   = model.FechaCompleta,
            Prevision       = model.Prevision,
            Repuesto        = model.Repuesto,
            TipoRepuesto    = model.TipoRepuesto,
        )

    @staticmethod
    def to_model(entity: ConsumoPrevision) -> ConsumoPrevisionModel:
        return ConsumoPrevisionModel(
            id              = entity.id,
            FechaCompleta   = entity.FechaCompleta,
            Prevision       = entity.Prevision,
            Repuesto        = entity.Repuesto,
            TipoRepuesto    = entity.TipoRepuesto,
        )