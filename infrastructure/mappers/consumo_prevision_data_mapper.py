from domain.entities.consumo_prevision_data import ConsumoPrevisionData
from infrastructure.db.models.consumo_prevision_data_model import ConsumoPrevisionDataModel


class ConsumoPrevisionDataMapper:
    @staticmethod
    def to_entity(model: ConsumoPrevisionDataModel) -> ConsumoPrevisionData:
        return ConsumoPrevisionData(
            id              = model.id,
            FechaCompleta   = model.FechaCompleta,
            Consumo         = model.Consumo,
            Repuesto        = model.Repuesto,
            TipoRepuesto    = model.TipoRepuesto,
        )

    @staticmethod
    def to_model(entity: ConsumoPrevisionData) -> ConsumoPrevisionDataModel:
        return ConsumoPrevisionDataModel(
            id              = entity.id,
            FechaCompleta   = entity.FechaCompleta,
            Consumo         = entity.Consumo,
            Repuesto        = entity.Repuesto,
            TipoRepuesto    = entity.TipoRepuesto,
        )