import pandas as pd

from domain.entities.maximos_minimos import MaximosMinimos
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from interfaces.viewmodel import ViewModel


class MaximosMinimosVM(ViewModel):
    def __init__(self, uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()) -> None:
        self.uow = uow


    def save_df(self, df) -> None:
        entities = [
            MaximosMinimos(
                id          = None,
                Familia     = row['Familia'],
                Articulo    = row['Articulo'],
                Repuesto    = row['Repuesto'],
                Minimo      = row['Minimo'],
                Maximo      = row['Maximo'],
            ) for index, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.maximos_minimos.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.maximos_minimos.get_all()
            return self.get_data(entities) if entities else pd.DataFrame()


    @staticmethod
    def get_data(entities) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "id": e.id,
                    "Familia": e.Familia,
                    "Articulo": e.Articulo,
                    "Repuesto": e.Repuesto,
                    "Minimo": e.Minimo,
                    "Maximo": e.Maximo
                }
                for e in entities
            ]
        )