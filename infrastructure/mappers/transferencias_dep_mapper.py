from domain.entities.transferencias_dep import TransferenciasEntreDepositos
from infrastructure.db.models.transferencias_dep_model import TransferenciasEntreDepositosModel
from interfaces.mapper import Mapper


class TransferenciasEntreDepositosMapper(Mapper):
    @staticmethod
    def to_entity(model: TransferenciasEntreDepositosModel) -> TransferenciasEntreDepositos:
        return TransferenciasEntreDepositos(
            id          = model.id,
            Repuesto    = model.Repuesto,
            Año         = model.Año,
            Cantidad    = model.Cantidad,
            Cabecera    = model.Cabecera,
        )

    @staticmethod
    def to_model(entity: TransferenciasEntreDepositos) -> TransferenciasEntreDepositosModel:
        return TransferenciasEntreDepositosModel(
            id          = entity.id,
            Repuesto    = entity.Repuesto,
            Año         = entity.Año,
            Cantidad    = entity.Cantidad,
            Cabecera    = entity.Cabecera,
        )
