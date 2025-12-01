from typing import Any

from domain.entities.parque_movil import ParqueMovil
from infrastructure.db.models.parque_movil_model import ParqueMovilModel
from interfaces.mapper import Mapper


class ParqueMovilMapper(Mapper):
    @staticmethod
    def to_entity(model: ParqueMovilModel) -> ParqueMovil:
        return ParqueMovil(
            id                  = model.id,
            FechaParqueMovil    = model.FechaParqueMovil,
            Linea               = model.Linea,
            Interno             = model.Interno,
            Dominio             = model.Dominio,
            Asientos            = model.Asientos,
            Marca               = model.Marca,
            Año                 = model.Año,
            Serie               = model.Serie,
            Chasis              = model.Chasis,
            Motor               = model.Motor,
            Carroceria          = model.Carroceria,
        )

    @staticmethod
    def to_model(entity: ParqueMovil) -> ParqueMovilModel:
        return ParqueMovilModel(
            id                  = entity.id,
            FechaParqueMovil    = entity.FechaParqueMovil,
            Linea               = entity.Linea,
            Interno             = entity.Interno,
            Dominio             = entity.Dominio,
            Asientos            = entity.Asientos,
            Marca               = entity.Marca,
            Año                 = entity.Año,
            Serie               = entity.Serie,
            Chasis              = entity.Chasis,
            Motor               = entity.Motor,
            Carroceria          = entity.Carroceria,
        )