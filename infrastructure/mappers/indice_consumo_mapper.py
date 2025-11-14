from domain.entities.indice_consumo import IndiceConsumo
from infrastructure.db.models.indice_consumo_model import IndiceConsumoModel


class IndiceConsumoMapper:
    @staticmethod
    def to_entity(model: IndiceConsumoModel) -> IndiceConsumo:
        return IndiceConsumo(
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
    def to_model(entity: IndiceConsumo) -> IndiceConsumoModel:
        return IndiceConsumoModel(
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