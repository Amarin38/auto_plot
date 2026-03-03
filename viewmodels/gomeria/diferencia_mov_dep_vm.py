import pandas as pd

from domain.entities.gomeria_diferencia_mov_dep import GomeriaDiferenciaMovEntreDep
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from interfaces.viewmodel import ViewModel


class DiferenciaMovimientosEntreDepositosVM(ViewModel):
    def __init__(self, uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()) -> None:
        self.uow = uow

    def save_df(self, df) -> None:
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
            ) for index, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.gomeria_diferencia_mov.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.gomeria_diferencia_mov.get_all()

            df = self.get_data(entities) if entities else pd.DataFrame()
            df["Diferencia Costos"] = df["Diferencia Costos"].fillna(0)

            return df


    @staticmethod
    def get_data(entities) -> pd.DataFrame:
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


