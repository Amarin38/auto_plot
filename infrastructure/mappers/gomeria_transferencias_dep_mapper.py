from domain.entities.gomeria_transferencias_dep import GomeriaTransferenciasEntreDep
from infrastructure.db.models.gomeria_transferencias_dep_model import GomeriaTransferenciasEntreDepModel
from interfaces.mapper import Mapper


class GomeriaTransferenciasEntreDepMapper(Mapper):
    @staticmethod
    def to_entity(model: GomeriaTransferenciasEntreDepModel) -> GomeriaTransferenciasEntreDep:
        return GomeriaTransferenciasEntreDep(
            id          = model.id,
            Repuesto    = model.Repuesto,
            Año         = model.Año,
            Cantidad    = model.Cantidad,
            Cabecera    = model.Cabecera,
        )

    @staticmethod
    def to_model(entity: GomeriaTransferenciasEntreDep) -> GomeriaTransferenciasEntreDepModel:
        return GomeriaTransferenciasEntreDepModel(
            id          = entity.id,
            Repuesto    = entity.Repuesto,
            Año         = entity.Año,
            Cantidad    = entity.Cantidad,
            Cabecera    = entity.Cabecera,
        )
