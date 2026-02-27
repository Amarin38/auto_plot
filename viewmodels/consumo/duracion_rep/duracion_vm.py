import pandas as pd

from domain.entities.duracion_repuestos import DuracionRepuestos
from infrastructure.repositories.duracion_repuestos_repository import DuracionRepuestosRepository


class DuracionRepuestosVM:
    def __init__(self) -> None:
        self.repo = DuracionRepuestosRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = DuracionRepuestos(
                id                          = None,
                Patente                     = row['Patente'],
                FechaCambio                 = row['FechaCambio'],
                Cambio                      = row['Cambio'],
                Cabecera                    = row['Cabecera'],
                Observaciones               = row['Observaciones'],
                Repuesto                    = row['Repuesto'],
                TipoRepuesto                = row['TipoRepuesto'],
                DuracionEnDias              = row['DuracionEnDias'],
                DuracionEnMeses             = row['DuracionEnMeses'],
                DuracionEnAños              = row['DuracionEnAños'],
                AñoPromedio                 = row['AñoPromedio'],
                DesviacionEstandar          = row['DesviacionEstandar'],
            )
            entities.append(entity)

        self.repo.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        entities = self.repo.get_all()
        return self.get_data(entities)


    def get_df_by_repuesto(self, repuesto: str) -> pd.DataFrame:
        entities = self.repo.get_by_repuesto(repuesto)
        df = self.get_data(entities)

        df["FechaCambio"] = pd.to_datetime(df["FechaCambio"], errors="coerce")
        return df


    @staticmethod
    def get_data(entities) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "id": e.id,
                    "Patente": e.Patente,
                    "FechaCambio": e.FechaCambio,
                    "Cambio": e.Cambio,
                    "Cabecera": e.Cabecera,
                    "Observaciones": e.Observaciones,
                    "Repuesto": e.Repuesto,
                    "TipoRepuesto": e.TipoRepuesto,
                    "DuracionEnDias": e.DuracionEnDias,
                    "DuracionEnMeses": e.DuracionEnMeses,
                    "DuracionEnAños": e.DuracionEnAños,
                    "AñoPromedio": e.AñoPromedio,
                    "DesviacionEstandar": e.DesviacionEstandar
                }
                for e in entities
            ]
        )