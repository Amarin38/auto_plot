from typing import Dict, Any

from multipledispatch import dispatch

import pandas as pd
from pandas import DataFrame

from domain.entities.json_config import JSONConfig
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from interfaces.viewmodel import ViewModel


class JSONConfigVM(ViewModel):
    def __init__(self, uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()) -> None:
        self.uow = uow


    def save_df(self, df) -> None:
        entities = [
            JSONConfig(
                id      = None,
                nombre  = row['nombre'],
                data    = row['data'],
            ) for index, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.json_config.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.json_config.get_all()
            return self.get_data(entities) if entities else pd.DataFrame()


    @dispatch(int)
    def get_df_by_id(self, _id: int) -> Dict[Any, Any]:
        with self.uow as uow:
            entity = uow.json_config.get_by_id(_id)
            return entity.data if entity else {}


    @dispatch(str)
    def get_df_by_id(self, nombre: str) -> Dict[Any, Any]:
        with self.uow as uow:
            entity = uow.json_config.get_by_id(nombre)
            return entity.data if entity else {}


    @staticmethod
    def get_data(entities) -> DataFrame:
        return pd.DataFrame([
            {
                "id": e.id,
                "nombre": e.nombre,
                "data": e.data,
            }
            for e in entities
        ])
