import pandas as pd

from domain.entities.falla_garantias import FallaGarantias
from infrastructure.repositories.falla_garantias_repository import FallaGarantiasRepository


class FallaGarantiasVM:
    def __init__(self) -> None:
        self.repo = FallaGarantiasRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = FallaGarantias(
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
