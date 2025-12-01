from domain.entities.consumo_desviacion_indices import ConsumoDesviacionIndices
from infrastructure.db.models.consumo_desviacion_indices_model import ConsumoDesviacionIndicesModel

class ConsumoDesviacionIndicesMapper:
    @staticmethod
    def to_entity(model: ConsumoDesviacionIndicesModel) -> ConsumoDesviacionIndices:
        return ConsumoDesviacionIndices(
            id                      = model.id,
            Cabecera                = model.Cabecera,
            TipoRepuesto            = model.TipoRepuesto,
            MediaRepuesto           = model.MediaRepuesto,
            MediaDeMediasRepuesto   = model.MediaDeMediasRepuesto,
            DiferenciaRepuesto      = model.DiferenciaRepuesto,
            DesviacionRepuesto      = model.DesviacionRepuesto,
            DesviacionRepuestoPor   = model.DesviacionRepuestoPor,
            MediaCabecera           = model.MediaCabecera,
            MediaDeMediasCabecera   = model.MediaDeMediasCabecera,
            DiferenciaCabecera      = model.DiferenciaCabecera,
            DesviacionCabecera      = model.DesviacionCabecera,
            DesviacionCabeceraPor   = model.DesviacionCabeceraPor,
            FechaCompleta           = model.FechaCompleta
        )

    @staticmethod
    def to_model(entity: ConsumoDesviacionIndices) -> ConsumoDesviacionIndicesModel:
        return ConsumoDesviacionIndicesModel(
            id                      = entity.id,
            Cabecera                = entity.Cabecera,
            TipoRepuesto            = entity.TipoRepuesto,
            MediaRepuesto           = entity.MediaRepuesto,
            MediaDeMediasRepuesto   = entity.MediaDeMediasRepuesto,
            DiferenciaRepuesto      = entity.DiferenciaRepuesto,
            DesviacionRepuesto      = entity.DesviacionRepuesto,
            DesviacionRepuestoPor   = entity.DesviacionRepuestoPor,
            MediaCabecera           = entity.MediaCabecera,
            MediaDeMediasCabecera   = entity.MediaDeMediasCabecera,
            DiferenciaCabecera      = entity.DiferenciaCabecera,
            DesviacionCabecera      = entity.DesviacionCabecera,
            DesviacionCabeceraPor   = entity.DesviacionCabeceraPor,
            FechaCompleta           = entity.FechaCompleta
        )