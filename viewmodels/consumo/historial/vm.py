import pandas as pd

from config.enums import RepuestoEnum
from domain.entities.historial_consumo import HistorialConsumo
from infrastructure.repositories.historial_consumo_repository import HistorialConsumoRepository


class HistorialConsumoVM:
    def __init__(self) -> None:
        self.repo = HistorialConsumoRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = HistorialConsumo(
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

        data = [
            {
                "id"            : e.id,
                "TipoRepuesto"  : e.TipoRepuesto,
                "Año"           : e.Año,
                "TotalConsumo"  : e.TotalConsumo,
                "FechaMin"      : e.FechaMin,
                "FechaMax"      : e.FechaMax,
            }
            for e in entities
        ]

        return pd.DataFrame(data)


    def get_df_tipo_repuesto(self, tipo_repuesto: RepuestoEnum) -> pd.DataFrame:
        entities = self.repo.get_by_tipo_rep(tipo_repuesto)

        data = [
            {
                "id"            : e.id,
                "TipoRepuesto"  : e.TipoRepuesto,
                "Año"           : e.Año,
                "TotalConsumo"  : e.TotalConsumo,
                "FechaMin"      : e.FechaMin,
                "FechaMax"      : e.FechaMax,
            }
            for e in entities
        ]

        return pd.DataFrame(data)