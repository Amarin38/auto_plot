from domain.entities.services.duracion_repuestos import DuracionRepuestos
from infrastructure.db.models.services.duracion_repuestos_model import DuracionRepuestosModel


class DuracionRepuestosMapper:
    @staticmethod
    def to_entity(model: DuracionRepuestosModel) -> DuracionRepuestos:
        return DuracionRepuestos(
            id                  = model.id,
            Patente             = model.Patente,
            FechaCambio         = model.FechaCambio,
            Cambio              = model.Cambio,
            Cabecera            = model.Cabecera,
            Observaciones       = model.Observaciones,
            Repuesto            = model.Repuesto,
            TipoRepuesto        = model.TipoRepuesto,
            DuracionEnDias      = model.DuracionEnDias,
            DuracionEnMeses     = model.DuracionEnMeses,
            DuracionEnAños      = model.DuracionEnAños,
            AñoPromedio         = model.AñoPromedio,
            DesviacionEstandar  = model.DesviacionEstandar
        )

    @staticmethod
    def to_model(entity: DuracionRepuestos) -> DuracionRepuestosModel:
        return DuracionRepuestosModel(
            id                  = entity.id,
            Patente             = entity.Patente,
            FechaCambio         = entity.FechaCambio,
            Cambio              = entity.Cambio,
            Cabecera            = entity.Cabecera,
            Observaciones       = entity.Observaciones,
            Repuesto            = entity.Repuesto,
            TipoRepuesto        = entity.TipoRepuesto,
            DuracionEnDias      = entity.DuracionEnDias,
            DuracionEnMeses     = entity.DuracionEnMeses,
            DuracionEnAños      = entity.DuracionEnAños,
            AñoPromedio         = entity.AñoPromedio,
            DesviacionEstandar  = entity.DesviacionEstandar
        )