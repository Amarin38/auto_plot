import pandas as pd

from domain.entities.gomeria.diferencia_mov_dep import GomeriaDiferenciaMovEntreDep
from domain.entities.gomeria.transferencias_dep import GomeriaTransferenciasEntreDep
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork


class TransferenciasEntreDepositosVM:
    def __init__(self, uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()) -> None:
        self.uow = uow

    def save_transferencias_df(self, df) -> None:
        entities = [
            GomeriaTransferenciasEntreDep(
                id          = None,
                Repuesto    = row["Repuesto"],
                Año         = row["Año"],
                Cantidad    = row["Cantidad"],
                Cabecera    = row["Cabecera"]
            ) for _, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.gomeria_transferencias.insert_many(entities)

    def save_diferencia_df(self, df) -> None:
        entities = [
            GomeriaDiferenciaMovEntreDep(
                id                  = None,
                Familia             = row["Familia"],
                Articulo            = row["Articulo"],
                Repuesto            = row["Repuesto"],
                Cantidad2024        = row["Cantidad2024"],
                CostoTotal2024      = row["CostoTotal2024"],
                Cantidad2025        = row["Cantidad2025"],
                CostoTotal2025      = row["CostoTotal2025"],
                DiferenciaAnual     = row["DiferenciaAnual"],
                DiferenciaDeCostos  = row["DiferenciaDeCostos"]
            ) for _, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.gomeria_diferencia_mov.insert_many(entities)


    def get_transferencias_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.gomeria_transferencias.get_all()
            return self.get_transferencias_data(entities) if entities else pd.DataFrame()

    def get_diferencia_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.gomeria_diferencia_mov.get_all()

            df = self.get_diferencia_data(entities) if entities else pd.DataFrame()
            df["Diferencia Costos"] = df["Diferencia Costos"].fillna(0)

            return df


    def get_transferencias_df_by_cabecera(self, cabecera: str) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.gomeria_transferencias.get_by_cabecera(cabecera)
            return self.get_transferencias_data(entities) if entities else pd.DataFrame()


    @staticmethod
    def get_transferencias_data(entities) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "id": e.id,
                    "Repuesto": e.Repuesto,
                    "Año": e.Año,
                    "Cantidad": e.Cantidad,
                    "Cabecera": e.Cabecera
                }
                for e in entities
            ]
        )

    @staticmethod
    def get_diferencia_data(entities) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "id": e.id,
                    "Familia": e.Familia,
                    "Articulo": e.Articulo,
                    "Repuesto": e.Repuesto,
                    "Consumo2024": e.Cantidad2024,
                    "Costo2024": e.CostoTotal2024,
                    "Consumo2025": e.Cantidad2025,
                    "Costo2025": e.CostoTotal2025,
                    "Diferencia Consumos": e.DiferenciaAnual,
                    "Diferencia Costos": e.DiferenciaDeCostos
                }
                for e in entities
            ]
        )
