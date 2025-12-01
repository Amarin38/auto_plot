import pandas as pd

from domain.entities.distribucion_normal import DistribucionNormal
from infrastructure.repositories.distribucion_normal_repository import DistribucionNormalRepository
from interfaces.viewmodel import ViewModel


class DistribucionNormalVM(ViewModel):
    def __init__(self) -> None:
        self.repo = DistribucionNormalRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = DistribucionNormal(
                id                          = None,
                Años                        = row['Años'],
                Cambio                      = row['Cambio'],
                Cabecera                    = row['Cabecera'],
                Repuesto                    = row['Repuesto'],
                TipoRepuesto                = row['TipoRepuesto'],
                AñoPromedio                 = row['AñoPromedio'],
                DesviacionEstandar          = row['DesviacionEstandar'],
                DistribucionNormal          = row['DistribucionNormal'],
            )
            entities.append(entity)

        self.repo.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        entities = self.repo.get_all()

        data = [
            {
                "id"                        : e.id,
                "Años"                      : e.Años,
                "Cambio"                    : e.Cambio,
                "Cabecera"                  : e.Cabecera,
                "Repuesto"                  : e.Repuesto,
                "TipoRepuesto"              : e.TipoRepuesto,
                "AñoPromedio"               : e.AñoPromedio,
                "DesviacionEstandar"        : e.DesviacionEstandar,
                "DistribucionNormal"        : e.DistribucionNormal
            }
            for e in entities
        ]

        return pd.DataFrame(data)


    def get_df_by_repuesto(self, repuesto: str) -> pd.DataFrame:
        entities = self.repo.get_by_repuesto(repuesto)

        data = [
            {
                "id": e.id,
                "Años": e.Años,
                "Cambio": e.Cambio,
                "Cabecera": e.Cabecera,
                "Repuesto": e.Repuesto,
                "TipoRepuesto": e.TipoRepuesto,
                "AñoPromedio": e.AñoPromedio,
                "DesviacionEstandar": e.DesviacionEstandar,
                "DistribucionNormal": e.DistribucionNormal
            }
            for e in entities
        ]

        return pd.DataFrame(data)