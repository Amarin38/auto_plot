import pandas as pd

from domain.entities.services.diferencia_movimientos_entre_depositos import DiferenciaMovimientosEntreDepositos
from infrastructure.repositories.services.diferencia_movimientos_entre_depositos_repository import \
    DiferenciaMovimientosEntreDepositosRepository
from interfaces.viewmodel import ViewModel


class DiferenciaMovimientosEntreDepositosVM(ViewModel):
    def __init__(self) -> None:
        self.repo = DiferenciaMovimientosEntreDepositosRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = DiferenciaMovimientosEntreDepositos(
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
                "Cantidad2024"          : e.Cantidad2024,
                "CostoTotal2024"        : e.CostoTotal2024,
                "Cantidad2025"          : e.Cantidad2025,
                "CostoTotal2025"        : e.CostoTotal2025,
                "DiferenciaAnual"        : e.DiferenciaAnual,
                "DiferenciaDeCostos"    : e.DiferenciaDeCostos
            }
            for e in entities
        ]

        return pd.DataFrame(data)