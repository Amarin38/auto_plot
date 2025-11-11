from domain.entities.common.datos_garantias import DatosGarantias
from infrastructure.db.models.common.datos_garantias_model import DatosGarantiasModel
from interfaces.mapper import Mapper


class DatosGarantiasMapper(Mapper):
    @staticmethod
    def to_entity(model: DatosGarantiasModel) -> DatosGarantias:
        return DatosGarantias(
            id                  = model.id,
            Año                 = model.Año,
            Mes                 = model.Mes,
            FechaIngreso        = model.FechaIngreso,
            FechaEnvio          = model.FechaEnvio,
            Cabecera            = model.Cabecera,
            Interno             = model.Interno,
            Codigo              = model.Codigo,
            Repuesto            = model.Repuesto,
            Cantidad            = model.Cantidad,
            FechaColocacion     = model.FechaColocacion,
            Detalle             = model.Detalle,
            Tipo                = model.Tipo,
            DiasColocado        = model.DiasColocado
        )

    @staticmethod
    def to_model(entity: DatosGarantias) -> DatosGarantiasModel:
        return DatosGarantiasModel(
            id                  = entity.id,
            Año                 = entity.Año,
            Mes                 = entity.Mes,
            FechaIngreso        = entity.FechaIngreso,
            FechaEnvio          = entity.FechaEnvio,
            Cabecera            = entity.Cabecera,
            Interno             = entity.Interno,
            Codigo              = entity.Codigo,
            Repuesto            = entity.Repuesto,
            Cantidad            = entity.Cantidad,
            FechaColocacion     = entity.FechaColocacion,
            Detalle             = entity.Detalle,
            Tipo                = entity.Tipo,
            DiasColocado        = entity.DiasColocado
        )