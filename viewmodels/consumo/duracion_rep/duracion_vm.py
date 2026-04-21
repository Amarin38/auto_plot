import pandas as pd

from domain.entities.consumo_duracion_repuestos import DuracionRepuestos
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork


class DuracionRepuestosVM:
    def __init__(self, uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()) -> None:
        self.uow = uow

    def save_df(self, df) -> None:
        entities = [
            DuracionRepuestos(
                id                  = None,
                Patente             = row['Patente'],
                FechaCambio         = row['FechaCambio'],
                Cambio              = row['Cambio'],
                Cabecera            = row['Cabecera'],
                Observaciones       = row['Observaciones'],
                Repuesto            = row['Repuesto'],
                TipoRepuesto        = row['TipoRepuesto'],
                DuracionEnDias      = row['DuracionEnDias'],
                DuracionEnMeses     = row['DuracionEnMeses'],
                DuracionEnAños      = row['DuracionEnAños'],
                AñoPromedio         = row['AñoPromedio'],
                DesviacionEstandar  = row['DesviacionEstandar'],
            ) for index, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.duracion_repuestos.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.duracion_repuestos.get_all()
            return self.get_data(entities) if entities else pd.DataFrame()


    def get_df_by_repuesto(self, repuesto: str) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.duracion_repuestos.get_by_repuesto(repuesto)
            df = self.get_data(entities) if entities else pd.DataFrame()

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