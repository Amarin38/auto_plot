import pandas as pd

from domain.entities.consumo.distribucion_normal import DistribucionNormal
from domain.entities.consumo.duracion_repuestos import DuracionRepuestos
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

    def save_distribucion_df(self, df) -> None:
        entities = [
            DistribucionNormal(
                id                  = None,
                Años                = row['Años'],
                Cambio              = row['Cambio'],
                Repuesto            = row['Repuesto'],
                TipoRepuesto        = row['TipoRepuesto'],
                AñoPromedio         = row['AñoPromedio'],
                DesviacionEstandar  = row['DesviacionEstandar'],
                DistribucionNormal  = row['DistribucionNormal'],
            ) for index, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.distribucion_normal.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.duracion_repuestos.get_all()
            return self.get_data(entities) if entities else pd.DataFrame()

    def get_distribucion_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.distribucion_normal.get_all()
            return self.get_distribucion_data(entities) if entities else pd.DataFrame()


    def get_df_by_repuesto(self, repuesto: str) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.duracion_repuestos.get_by_repuesto(repuesto)
            df = self.get_data(entities) if entities else pd.DataFrame()

            if not df.empty:
                df["FechaCambio"] = pd.to_datetime(df["FechaCambio"], errors="coerce")
            return df


    def get_distribucion_df_by_repuesto(self, repuesto: str) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.distribucion_normal.get_by_repuesto(repuesto)
            return self.get_distribucion_data(entities) if entities else pd.DataFrame()


    def get_repuestos(self) -> pd.Series:
        with self.uow as uow:
            return uow.duracion_repuestos.get_repuestos()


    @staticmethod
    def get_data(entities) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "id": e.id,
                    "Patente": e.Patente,
                    "FechaCambio": e.FechaCambio,
                    "Cambio": e.Cambio,
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

    @staticmethod
    def get_distribucion_data(entities) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "id": e.id,
                    "Años": e.Años,
                    "Cambio": e.Cambio,
                    "Repuesto": e.Repuesto,
                    "TipoRepuesto": e.TipoRepuesto,
                    "AñoPromedio": e.AñoPromedio,
                    "DesviacionEstandar": e.DesviacionEstandar,
                    "DistribucionNormal": e.DistribucionNormal
                }
                for e in entities
            ]
        )