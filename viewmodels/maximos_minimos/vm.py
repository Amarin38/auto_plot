import pandas as pd

from domain.entities.maximos_minimos import MaximosMinimos
from infrastructure.repositories.maximos_minimos_repository import MaximosMinimosRepository
from interfaces.viewmodel import ViewModel


class MaximosMinimosVM(ViewModel):
    def __init__(self) -> None:
        self.repo = MaximosMinimosRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = MaximosMinimos(
                id          = None,
                Familia     = row['Familia'],
                Articulo    = row['Articulo'],
                Repuesto    = row['Repuesto'],
                Minimo      = row['Minimo'],
                Maximo      = row['Maximo'],
            )
            entities.append(entity)

        self.repo.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        entities = self.repo.get_all()
        return self.get_data(entities)


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