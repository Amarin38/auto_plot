import pandas as pd

from domain.entities.prevision import Prevision
from infrastructure.repositories.prevision_repository import PrevisionRepository


class PrevisionVM:
    def __init__(self) -> None:
        self.repo = PrevisionRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = Prevision(
                id              = None,
                FechaCompleta   = row['FechaCompleta'],
                Prevision       = row['Prevision'],
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
                "Prevision"         : e.Prevision,
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
                "Prevision"         : e.Prevision,
                "Repuesto"          : e.Repuesto,
                "TipoRepuesto"      : e.TipoRepuesto,
            }
            for e in entities
        ]

        return pd.DataFrame(data)
