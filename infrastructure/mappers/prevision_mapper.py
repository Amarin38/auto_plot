from domain.entities.prevision import Prevision
from infrastructure.db.models.prevision_model import PrevisionModel


class PrevisionMapper:
    @staticmethod
    def to_entity(model: PrevisionModel) -> Prevision:
        return Prevision(
            id              = model.id,
            FechaCompleta   = model.FechaCompleta,
            Prevision       = model.Prevision,
            Repuesto        = model.Repuesto,
            TipoRepuesto    = model.TipoRepuesto,
        )

    @staticmethod
    def to_model(entity: Prevision) -> PrevisionModel:
        return PrevisionModel(
            id              = entity.id,
            FechaCompleta   = entity.FechaCompleta,
            Prevision       = entity.Prevision,
            Repuesto        = entity.Repuesto,
            TipoRepuesto    = entity.TipoRepuesto,
        )