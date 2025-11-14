from domain.entities.diferencia_mov_dep import DiferenciaMovimientosEntreDepositos
from infrastructure.db.models.diferencia_mov_dep_model import \
    DiferenciaMovimientosEntreDepositosModel
from interfaces.mapper import Mapper


class DiferenciaMovimientosEntreDepositosMapper(Mapper):
    @staticmethod
    def to_entity(model: DiferenciaMovimientosEntreDepositosModel) -> DiferenciaMovimientosEntreDepositos:
        return DiferenciaMovimientosEntreDepositos(
            id                  = model.id,
            Familia             = model.Familia,
            Articulo            = model.Articulo,
            Repuesto            = model.Repuesto,
            Cantidad2024        = model.Cantidad2024,
            CostoTotal2024      = model.CostoTotal2024,
            Cantidad2025        = model.Cantidad2025,
            CostoTotal2025      = model.CostoTotal2025,
            DiferenciaAnual     = model.DiferenciaAnual,
            DiferenciaDeCostos  = model.DiferenciaDeCostos,
        )

    @staticmethod
    def to_model(entity: DiferenciaMovimientosEntreDepositos) -> DiferenciaMovimientosEntreDepositosModel:
        return DiferenciaMovimientosEntreDepositosModel(
            id                  = entity.id,
            Familia             = entity.Familia,
            Articulo            = entity.Articulo,
            Repuesto            = entity.Repuesto,
            Cantidad2024        = entity.Cantidad2024,
            CostoTotal2024      = entity.CostoTotal2024,
            Cantidad2025        = entity.Cantidad2025,
            CostoTotal2025      = entity.CostoTotal2025,
            DiferenciaAnual     = entity.DiferenciaAnual,
            DiferenciaDeCostos  = entity.DiferenciaDeCostos,
        )