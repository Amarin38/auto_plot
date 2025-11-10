from domain.entities.services.desviacion_indices import DesviacionIndices
from infrastructure.db.models.services.desviacion_indices_model import DesviacionIndicesModel

class DesviacionIndicesMapper:
    @staticmethod
    def to_entity(model: DesviacionIndicesModel) -> DesviacionIndices:
        return DesviacionIndices(
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
    def to_model(entity: DesviacionIndices) -> DesviacionIndicesModel:
        return DesviacionIndicesModel(
            id              = entity.id,
            Cabecera        = entity.Cabecera,
            MediaCabecera   = entity.MediaCabecera,
            MediaDeMedias   = entity.MediaDeMedias,
            Diferencia      = entity.Diferencia,
            Desviacion      = entity.Desviacion,
            DesviacionPor   = entity.DesviacionPor,
            FechaCompleta   = entity.FechaCompleta
        )