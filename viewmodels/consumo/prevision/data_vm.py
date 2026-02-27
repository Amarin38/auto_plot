import pandas as pd

from config.constants_common import FILE_STRFTIME_YMD
from domain.entities.consumo_prevision_data import ConsumoPrevisionData
from infrastructure.repositories.consumo_prevision_data_repository import ConsumoPrevisionDataRepository


class PrevisionDataVM:
    def __init__(self) -> None:
        self.repo = ConsumoPrevisionDataRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = ConsumoPrevisionData(
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
        return self.get_data(entities)


    def get_df_by_tipo_repuesto(self, tipo_rep: str) -> pd.DataFrame:
        entities = self.repo.get_by_tipo_repuesto(tipo_rep)
        df = self.get_data(entities)

        df['FechaCompleta'] = pd.to_datetime(df['FechaCompleta'], format=FILE_STRFTIME_YMD)

        return df


    @staticmethod
    def get_data(entities) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "id": e.id,
                    "FechaCompleta": e.FechaCompleta,
                    "Consumo": e.Consumo,
                    "Repuesto": e.Repuesto,
                    "TipoRepuesto": e.TipoRepuesto,
                }
                for e in entities
            ]
        )