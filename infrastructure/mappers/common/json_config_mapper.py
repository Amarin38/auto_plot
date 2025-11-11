from typing import Any

from domain.entities.common.json_config import JSONConfig
from infrastructure.db.models.common.json_config_model import JSONConfigModel
from interfaces.mapper import Mapper


class JSONConfigMapper(Mapper):
    @staticmethod
    def to_entity(model: JSONConfigModel) -> JSONConfig:
        return JSONConfig(
            id      = model.id,
            nombre  = model.nombre,
            data    = model.data
        )

    @staticmethod
    def to_model(entity: JSONConfig) -> JSONConfigModel:
        return JSONConfigModel(
            id      = entity.id,
            nombre  = entity.nombre,
            data    = entity.data
        )