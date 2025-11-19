from domain.entities.gomeria_diferencia_mov_dep import GomeriaDiferenciaMovEntreDep
from infrastructure.db.models.gomeria_diferencia_mov_dep_model import \
    GomeriaDiferenciaMovEntreDepModel
from interfaces.mapper import Mapper


class GomeriaDiferenciaMovEntreDepMapper(Mapper):
    @staticmethod
    def to_entity(model: GomeriaDiferenciaMovEntreDepModel) -> GomeriaDiferenciaMovEntreDep:
        return GomeriaDiferenciaMovEntreDep(
            id                  = model.id,
            Familia             = model.Familia,
            Articulo            = model.Articulo,
            Repuesto            = model.Repuesto,
            Cantidad2024        = model.Cantidad2024,
            CostoTotal2024      = model.CostoTotal2024,
            Cantidad2025        = model.Cantidad2025,
            CostoTotal2025      = model.CostoTotal2025,
            DiferenciaAnual     = model.DiferenciaAnual,
            DiferenciaDeCostos  = model.DiferenciaDeCostos,
        )

    @staticmethod
    def to_model(entity: GomeriaDiferenciaMovEntreDep) -> GomeriaDiferenciaMovEntreDepModel:
        return GomeriaDiferenciaMovEntreDepModel(
            id                  = entity.id,
            Familia             = entity.Familia,
            Articulo            = entity.Articulo,
            Repuesto            = entity.Repuesto,
            Cantidad2024        = entity.Cantidad2024,
            CostoTotal2024      = entity.CostoTotal2024,
            Cantidad2025        = entity.Cantidad2025,
            CostoTotal2025      = entity.CostoTotal2025,
            DiferenciaAnual     = entity.DiferenciaAnual,
            DiferenciaDeCostos  = entity.DiferenciaDeCostos,
        )