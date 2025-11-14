from domain.entities.consumo_garantias import ConsumoGarantias
from infrastructure.db.models.consumo_garantias_model import ConsumoGarantiasModel

class ConsumoGarantiasMapper:
    @staticmethod
    def to_entity(model: ConsumoGarantiasModel) -> ConsumoGarantias:
        return ConsumoGarantias(
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
    def to_model(entity: ConsumoGarantias) -> ConsumoGarantiasModel:
        return ConsumoGarantiasModel(
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
        