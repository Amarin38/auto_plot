from domain.entities.consumo_desviacion_indices import ConsumoDesviacionIndices
from infrastructure.db.models.consumo_desviacion_indices_model import ConsumoDesviacionIndicesModel

class ConsumoDesviacionIndicesMapper:
    @staticmethod
    def to_entity(model: ConsumoDesviacionIndicesModel) -> ConsumoDesviacionIndices:
        return ConsumoDesviacionIndices(
            id              = model.id,
            Cabecera        = model.Cabecera,
            MediaCabecera   = model.MediaCabecera,
            MediaDeMedias   = model.MediaDeMedias,
            Diferencia      = model.Diferencia,
            Desviacion      = model.Desviacion,
            DesviacionPor   = model.DesviacionPor,
            FechaCompleta   = model.FechaCompleta
        )

    @staticmethod
    def to_model(entity: ConsumoDesviacionIndices) -> ConsumoDesviacionIndicesModel:
        return ConsumoDesviacionIndicesModel(
            id              = entity.id,
            Cabecera        = entity.Cabecera,
            MediaCabecera   = entity.MediaCabecera,
            MediaDeMedias   = entity.MediaDeMedias,
            Diferencia      = entity.Diferencia,
            Desviacion      = entity.Desviacion,
            DesviacionPor   = entity.DesviacionPor,
            FechaCompleta   = entity.FechaCompleta
        )