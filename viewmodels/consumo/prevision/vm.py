import pandas as pd

from config.constants_common import FILE_STRFTIME_YMD
from domain.entities.consumo_prevision import ConsumoPrevision
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork


class PrevisionVM:
    def __init__(self, uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()) -> None:
        self.uow = uow


    def save_df(self, df) -> None:
        entities = [
            ConsumoPrevision(
                id              = None,
                FechaCompleta   = row['FechaCompleta'],
                Prevision       = row['ConsumoPrevision'],
                Repuesto        = row['Repuesto'],
                TipoRepuesto    = row['TipoRepuesto'],
            ) for _, row in df.iterrows()

        ]

        with self.uow as uow:
            uow.consumo_prevision.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.consumo_prevision.get_all()
            return self.get_data(entities) if entities else pd.DataFrame()


    def get_df_by_tipo_repuesto(self, tipo_rep: str) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.consumo_prevision.get_by_tipo_repuesto(tipo_rep)
            df = self.get_data(entities) if entities else pd.DataFrame()

            df['FechaCompleta'] = pd.to_datetime(df['FechaCompleta'], format=FILE_STRFTIME_YMD)
            return df


    @staticmethod
    def get_data(entities) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "id": e.id,
                    "FechaCompleta": e.FechaCompleta,
                    "ConsumoPrevision": e.Prevision,
                    "Repuesto": e.Repuesto,
                    "TipoRepuesto": e.TipoRepuesto,
                }
                for e in entities
            ]
        )