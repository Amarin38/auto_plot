import pandas as pd

from config.enums import RepuestoEnum
from domain.entities.consumo_historial import ConsumoHistorial
from infrastructure.repositories.consumo_historial_repository import ConsumoHistorialRepository


class HistorialConsumoVM:
    def __init__(self) -> None:
        self.repo = ConsumoHistorialRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = ConsumoHistorial(
                id              = None,
                TipoRepuesto    = row['TipoRepuesto'],
                Año             = row['Año'],
                TotalConsumo    = row['TotalConsumo'],
                FechaMin        = row['FechaMin'],
                FechaMax        = row['FechaMax'],
            )
            entities.append(entity)

        self.repo.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        entities = self.repo.get_all()
        return self.get_data(entities)


    def get_df_tipo_repuesto(self, tipo_repuesto: RepuestoEnum) -> pd.DataFrame:
        entities = self.repo.get_by_tipo_rep(tipo_repuesto)
        return self.get_data(entities)


    @staticmethod
    def get_data(entities) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "id": e.id,
                    "TipoRepuesto": e.TipoRepuesto,
                    "Año": e.Año,
                    "TotalConsumo": e.TotalConsumo,
                    "FechaMin": e.FechaMin,
                    "FechaMax": e.FechaMax,
                }
                for e in entities
            ]
        )