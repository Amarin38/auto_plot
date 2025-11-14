from domain.entities.prevision_data import PrevisionData
from infrastructure.db.models.prevision_data_model import PrevisionDataModel


class PrevisionDataMapper:
    @staticmethod
    def to_entity(model: PrevisionDataModel) -> PrevisionData:
        return PrevisionData(
            id              = model.id,
            FechaCompleta   = model.FechaCompleta,
            Consumo         = model.Consumo,
            Repuesto        = model.Repuesto,
            TipoRepuesto    = model.TipoRepuesto,
        )

    @staticmethod
    def to_model(entity: PrevisionData) -> PrevisionDataModel:
        return PrevisionDataModel(
            id              = entity.id,
            FechaCompleta   = entity.FechaCompleta,
            Consumo         = entity.Consumo,
            Repuesto        = entity.Repuesto,
            TipoRepuesto    = entity.TipoRepuesto,
        )