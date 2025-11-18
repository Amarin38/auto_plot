from domain.entities.consumo_obligatorio import ConsumoObligatorio
from infrastructure.db.models.consumo_obligatorio_model import ConsumoObligatorioModel
from interfaces.mapper import Mapper


class ConsumoObligatorioMapper(Mapper):
    @staticmethod
    def to_entity(model: ConsumoObligatorioModel) -> ConsumoObligatorio:
        return ConsumoObligatorio(
            id                  = model.id,
            Cabecera            = model.Cabecera,
            Repuesto            = model.Repuesto,
            Año2023             = model.Año2023,
            Año2024             = model.Año2024,
            Año2025             = model.Año2025,
            MinimoObligatorio   = model.MinimoObligatorio,
            UltimaFecha         = model.UltimaFecha,
        )

    @staticmethod
    def to_model(entity: ConsumoObligatorio) -> ConsumoObligatorioModel:
        return ConsumoObligatorioModel(
            id                  = entity.id,
            Cabecera            = entity.Cabecera,
            Repuesto            = entity.Repuesto,
            Año2023             = entity.Año2023,
            Año2024             = entity.Año2024,
            Año2025             = entity.Año2025,
            MinimoObligatorio   = entity.MinimoObligatorio,
            UltimaFecha         = entity.UltimaFecha,
        )