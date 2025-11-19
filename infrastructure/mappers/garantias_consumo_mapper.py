from domain.entities.garantias_consumo import GarantiasConsumo
from infrastructure.db.models.garantias_consumo_model import GarantiasConsumoModel

class GarantiasConsumoMapper:
    @staticmethod
    def to_entity(model: GarantiasConsumoModel) -> GarantiasConsumo:
        return GarantiasConsumo(
            id                          = model.id,
            Cabecera                    = model.Cabecera,
            Repuesto                    = model.Repuesto,
            TipoRepuesto                = model.TipoRepuesto,
            Garantia                    = model.Garantia,
            Transferencia               = model.Transferencia,
            Total                       = model.Total,
            PorcentajeTransferencia     = model.PorcentajeTransferencia,
            PorcentajeGarantia          = model.PorcentajeGarantia,
        )

    @staticmethod
    def to_model(entity: GarantiasConsumo) -> GarantiasConsumoModel:
        return GarantiasConsumoModel(
            id                          = entity.id,
            Cabecera                    = entity.Cabecera,
            Repuesto                    = entity.Repuesto,
            TipoRepuesto                = entity.TipoRepuesto,
            Garantia                    = entity.Garantia,
            Transferencia               = entity.Transferencia,
            Total                       = entity.Total,
            PorcentajeTransferencia     = entity.PorcentajeTransferencia,
            PorcentajeGarantia          = entity.PorcentajeGarantia,
        )
        