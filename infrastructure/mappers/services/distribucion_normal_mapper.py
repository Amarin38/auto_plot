from domain.entities.services.distribucion_normal import DistribucionNormal
from infrastructure.db.models.services.distribucion_normal_model import DistribucionNormalModel


class DistribucionNormalMapper:
    @staticmethod
    def to_entity(model: DistribucionNormalModel) -> DistribucionNormal:
        return DistribucionNormal(
            id                  = model.id,
            Años                = model.Años,
            Cambio              = model.Cambio,
            Cabecera            = model.Cabecera,
            Repuesto            = model.Repuesto,
            TipoRepuesto        = model.TipoRepuesto,
            AñoPromedio         = model.AñoPromedio,
            DesviacionEstandar  = model.DesviacionEstandar,
            DistribucionNormal  = model.DistribucionNormal
        )

    @staticmethod
    def to_model(entity: DistribucionNormal) -> DistribucionNormalModel:
        return DistribucionNormalModel(
            id                  = entity.id,
            Años                = entity.Años,
            Cambio              = entity.Cambio,
            Cabecera            = entity.Cabecera,
            Repuesto            = entity.Repuesto,
            TipoRepuesto        = entity.TipoRepuesto,
            AñoPromedio         = entity.AñoPromedio,
            DesviacionEstandar  = entity.DesviacionEstandar,
            DistribucionNormal  = entity.DistribucionNormal
        )