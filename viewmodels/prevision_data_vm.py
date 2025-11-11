import pandas as pd

from domain.entities.services.prevision_data import PrevisionData
from infrastructure.repositories.services.prevision_data_repository import PrevisionDataRepository


class PrevisionDataVM:
    def __init__(self) -> None:
        self.repo = PrevisionDataRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = PrevisionData(
                id                  = None,
                FechaCompleta       = row['FechaCompleta'],
                Consumo             = row['Consumo'],
                Repuesto            = row['Repuesto'],
                TipoRepuesto        = row['TipoRepuesto'],
            )
            entities.append(entity)

        self.repo.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        entities = self.repo.get_all()

        data = [
            {
                "id"                : e.id,
                "FechaCompleta"     : e.FechaCompleta,
                "Consumo"           : e.Consumo,
                "Repuesto"          : e.Repuesto,
                "TipoRepuesto"      : e.TipoRepuesto,
            }
            for e in entities
        ]

        return pd.DataFrame(data)


    def get_df_by_tipo_repuesto(self, tipo_rep: str) -> pd.DataFrame:
        entities = self.repo.get_by_tipo_repuesto(tipo_rep)

        data = [
            {
                "id"                : e.id,
                "FechaCompleta"     : e.FechaCompleta,
                "Consumo"           : e.Consumo,
                "Repuesto"          : e.Repuesto,
                "TipoRepuesto"      : e.TipoRepuesto,
            }
            for e in entities
        ]

        return pd.DataFrame(data)