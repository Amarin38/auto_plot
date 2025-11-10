from domain.entities.services.maximos_minimos import MaximosMinimos
from infrastructure.db.models.services.maximos_minimos_model import MaximosMinimosModel


class MaximosMinimosMapper:
    @staticmethod
    def to_entity(model: MaximosMinimosModel) -> MaximosMinimos:
        return MaximosMinimos(
            id          = model.id,
            Familia     = model.Familia,
            Articulo    = model.Articulo,
            Repuesto    = model.Repuesto,
            Minimo      = model.Minimo,
            Maximo      = model.Maximo
        )

    @staticmethod
    def to_model(entity: MaximosMinimos) -> MaximosMinimosModel:
        return MaximosMinimosModel(
            id = entity.id,
            Familia = entity.Familia,
            Articulo = entity.Articulo,
            Repuesto = entity.Repuesto,
            Minimo = entity.Minimo,
            Maximo = entity.Maximo
        )