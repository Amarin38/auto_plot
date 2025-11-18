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
                CochesDuermen       = row['CochesDuermen'],
                CochesDuermenNuevo  = row['CochesDuermenNuevo'],
                CochesSinScania     = row['CochesSinScania'],
            )
            entities.append(entity)

        self.repo.insert_many(entities)

    def get_df(self) -> pd.DataFrame:
        entities = self.repo.get_all()

        data = [
            {
                "id"                    : e.id,
                "Cabecera"              : e.Cabecera,
                "CochesDuermen"         : e.CochesDuermen,
                "CochesDuermenNuevo"    : e.CochesDuermenNuevo,
                "CochesSinScania"       : e.CochesSinScania
            }
            for e in entities
        ]

        return pd.DataFrame(data)