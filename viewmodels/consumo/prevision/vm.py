import pandas as pd

from domain.entities.consumo_prevision import ConsumoPrevision
from infrastructure.repositories.consumo_prevision_repository import ConsumoPrevisionRepository


class PrevisionVM:
    def __init__(self) -> None:
        self.repo = ConsumoPrevisionRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = ConsumoPrevision(
                id              = None,
                FechaCompleta   = row['FechaCompleta'],
                Prevision       = row['ConsumoPrevision'],
                Repuesto        = row['Repuesto'],
                TipoRepuesto    = row['TipoRepuesto'],
            )
            entities.append(entity)

        self.repo.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        entities = self.repo.get_all()

        data = [
            {
                "id"                : e.id,
                "FechaCompleta"     : e.FechaCompleta,
                "ConsumoPrevision"         : e.Prevision,
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
                "ConsumoPrevision"         : e.Prevision,
                "Repuesto"          : e.Repuesto,
                "TipoRepuesto"      : e.TipoRepuesto,
            }
            for e in entities
        ]

        return pd.DataFrame(data)
