from typing import Any

from domain.entities.common.coches_cabecera import CochesCabecera
from infrastructure.db.models.common.coches_cabecera_model import CochesCabeceraModel
from interfaces.mapper import Mapper


class CochesCabeceraMapper(Mapper):
    @staticmethod
    def to_entity(model: CochesCabeceraModel) -> CochesCabecera:
        return CochesCabecera(
            id                  = model.id,
            Cabecera            = model.Cabecera,
            CantidadCoches      = model.CantidadCoches,
            CantidadCochesNew   = model.CantidadCochesNew,
        )

    @staticmethod
    def to_model(entity: CochesCabecera) -> CochesCabeceraModel:
        return CochesCabeceraModel(
            id                  = entity.id,
            Cabecera            = entity.Cabecera,
            CantidadCoches      = entity.CantidadCoches,
            CantidadCochesNew   = entity.CantidadCochesNew,
        )