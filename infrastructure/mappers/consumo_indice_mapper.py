from domain.entities.consumo_indice import ConsumoIndice
from infrastructure.db.models.consumo_indice_model import ConsumoIndiceModel


class ConsumoIndiceMapper:
    @staticmethod
    def to_entity(model: ConsumoIndiceModel) -> ConsumoIndice:
        return ConsumoIndice(
            id              = model.id,
            Cabecera        = model.Cabecera,
            Repuesto        = model.Repuesto,
            TipoRepuesto    = model.TipoRepuesto,
            TotalConsumo    = model.TotalConsumo,
            TotalCoste      = model.TotalCoste,
            IndiceConsumo   = model.IndiceConsumo,
            UltimaFecha     = model.UltimaFecha,
            TipoOperacion   = model.TipoOperacion,
        )

    @staticmethod
    def to_model(entity: ConsumoIndice) -> ConsumoIndiceModel:
        return ConsumoIndiceModel(
            id              = entity.id,
            Cabecera        = entity.Cabecera,
            Repuesto        = entity.Repuesto,
            TipoRepuesto    = entity.TipoRepuesto,
            TotalConsumo    = entity.TotalConsumo,
            TotalCoste      = entity.TotalCoste,
            IndiceConsumo   = entity.IndiceConsumo,
            UltimaFecha     = entity.UltimaFecha,
            TipoOperacion   = entity.TipoOperacion,
        )