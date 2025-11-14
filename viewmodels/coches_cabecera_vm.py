import pandas as pd

from domain.entities.coches_cabecera import CochesCabecera
from infrastructure.repositories.coches_cabecera_repository import CochesCabeceraRepository
from interfaces.viewmodel import ViewModel


class CochesCabeceraVM(ViewModel):
    def __init__(self) -> None:
        self.repo = CochesCabeceraRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = CochesCabecera(
                id                  = None,
                Cabecera            = row['Cabecera'],
                CantidadCoches      = row['CantidadCoches'],
                CantidadCochesNew   = row['CantidadCochesNew']
            )
            entities.append(entity)

        self.repo.insert_many(entities)

    def get_df(self) -> pd.DataFrame:
        entities = self.repo.get_all()

        data = [
            {
                "id"                    : e.id,
                "Cabecera"              : e.Cabecera,
                "CantidadCoches"        : e.CantidadCoches,
                "CantidadCochesNew"     : e.CantidadCochesNew
            }
            for e in entities
        ]

        return pd.DataFrame(data)