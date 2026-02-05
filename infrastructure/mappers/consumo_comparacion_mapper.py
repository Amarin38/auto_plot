from domain.entities.consumo_comparacion import ConsumoComparacion
from infrastructure.db.models.consumo_comparacion_model import ConsumoComparacionModel


class ConsumoComparacionMapper:
    @staticmethod
    def to_entity(model: ConsumoComparacionModel) -> ConsumoComparacion:
        return ConsumoComparacion(
            id              = model.id,
            Familia         = model.Familia,
            Articulo        = model.Articulo,
            Repuesto        = model.Repuesto,
            TipoRepuesto    = model.TipoRepuesto,
            Cabecera        = model.Cabecera,
            Consumo         = model.Consumo,
            Gasto           = model.Gasto,
            FechaCompleta   = model.FechaCompleta,
            PeriodoID       = model.PeriodoID,
        )

    @staticmethod
    def to_model(entity: ConsumoComparacion) -> ConsumoComparacionModel:
        return ConsumoComparacionModel(
            id              = entity.id,
            Familia         = entity.Familia,
            Articulo        = entity.Articulo,
            Repuesto        = entity.Repuesto,
            TipoRepuesto    = entity.TipoRepuesto,
            Cabecera        = entity.Cabecera,
            Consumo         = entity.Consumo,
            Gasto           = entity.Gasto,
            FechaCompleta   = entity.FechaCompleta,
            PeriodoID       = entity.PeriodoID,
        )