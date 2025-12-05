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
            Año                 = model.Año,
            ChasisMarca         = model.ChasisMarca,
            ChasisModelo        = model.ChasisModelo,
            ChasisNum           = model.ChasisNum,
            MotorMarca          = model.MotorMarca,
            MotorModelo         = model.MotorModelo,
            MotorNum            = model.MotorNum,
            Carroceria          = model.Carroceria
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
            Año                 = entity.Año,
            ChasisMarca         = entity.ChasisMarca,
            ChasisModelo        = entity.ChasisModelo,
            ChasisNum           = entity.ChasisNum,
            MotorMarca          = entity.MotorMarca,
            MotorModelo         = entity.MotorModelo,
            MotorNum            = entity.MotorNum,
            Carroceria          = entity.Carroceria,
        )