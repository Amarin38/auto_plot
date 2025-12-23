import pandas as pd
from babel.numbers import format_decimal

from domain.entities.gomeria_diferencia_mov_dep import GomeriaDiferenciaMovEntreDep
from infrastructure.repositories.gomeria_diferencia_mov_dep_repository import \
    GomeriaDiferenciaMovEntreDepRepository
from interfaces.viewmodel import ViewModel


class DiferenciaMovimientosEntreDepositosVM(ViewModel):
    def __init__(self) -> None:
        self.repo = GomeriaDiferenciaMovEntreDepRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = GomeriaDiferenciaMovEntreDep(
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
            )
            entities.append(entity)

        self.repo.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        entities = self.repo.get_all()

        data = [
            {
                "id"                    : e.id,
                "Familia"               : e.Familia,
                "Articulo"              : e.Articulo,
                "Repuesto"              : e.Repuesto,
                "Consumo2024"           : e.Cantidad2024,
                "Costo2024"             : e.CostoTotal2024,
                "Consumo2025"           : e.Cantidad2025,
                "Costo2025"             : e.CostoTotal2025,
                "Diferencia Consumos"   : e.DiferenciaAnual,
                "Diferencia Costos"     : e.DiferenciaDeCostos
            }
            for e in entities
        ]

        df = pd.DataFrame(data)
        df["Diferencia Costos"] = df["Diferencia Costos"].fillna(0)

        return df