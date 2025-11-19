import pandas as pd

from domain.entities.garantias_falla import GarantiasFalla
from infrastructure.repositories.garantias_falla_repository import GarantiasFallaRepository


class FallaGarantiasVM:
    def __init__(self) -> None:
        self.repo = GarantiasFallaRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = GarantiasFalla(
                id                      = None,
                Cabecera                = row['Cabecera'],
                Repuesto                = row['Repuesto'],
                TipoRepuesto            = row['TipoRepuesto'],
                PromedioTiempoFalla     = row['PromedioTiempoFalla'],
            )
            entities.append(entity)

        self.repo.insert_many(entities) # type: ignore


    def get_df(self) -> pd.DataFrame:
        entities = self.repo.get_all()

        data = [
            {
                "id"                    :e.id,
                "Cabecera"              :e.Cabecera,
                "Repuesto"              :e.Repuesto,
                "TipoRepuesto"          :e.TipoRepuesto,
                "PromedioTiempoFalla"   :e.PromedioTiempoFalla
            }
            for e in entities
        ]

        return pd.DataFrame(data)


    def get_df_by_tipo_rep_and_cabecera(self, tipo_repuesto: str, cabecera: str) -> pd.DataFrame:
        entities = self.repo.get_by_tipo_rep_and_cabecera(tipo_repuesto, cabecera)

        data = [
            {
                "id"                    : e.id,
                "Cabecera"              : e.Cabecera,
                "Repuesto"              : e.Repuesto,
                "TipoRepuesto"          : e.TipoRepuesto,
                "PromedioTiempoFalla"   : e.PromedioTiempoFalla
            }
            for e in entities
        ]

        return pd.DataFrame(data)
