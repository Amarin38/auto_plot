from typing import Dict, Any

from multipledispatch import dispatch

import pandas as pd

from domain.entities.common.json_config import JSONConfig
from infrastructure.repositories.common.json_config_repository import JSONConfigRepository
from interfaces.viewmodel import ViewModel


class JSONConfigVM(ViewModel):
    def __init__(self) -> None:
        self.repo = JSONConfigRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = JSONConfig(
                id=None,
                nombre=row['nombre'],
                data=row['data'],
            )
            entities.append(entity)

        self.repo.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        entities = self.repo.get_all()

        data = [
            {
                "id": e.id,
                "nombre": e.nombre,
                "data": e.data,
            }
            for e in entities
        ]

        return pd.DataFrame(data)


    @dispatch(int)
    def get_df_by_id(self, _id: int) -> Dict[Any, Any]:
        entity = self.repo.get_by_id(_id)

        if entity is not None:
            return entity.data
        return {}


    @dispatch(str)
    def get_df_by_id(self, nombre: str) -> Dict[Any, Any]:
        entity = self.repo.get_by_id(nombre)

        if entity is not None:
            return entity.data
        return {}
