import pandas as pd

from domain.entities.transferencias_dep import TransferenciasEntreDepositos
from infrastructure.repositories.transferencias_dep_repository import \
    TransferenciasEntreDepositosRepository
from interfaces.viewmodel import ViewModel


class TransferenciasEntreDepositosVM(ViewModel):
    def __init__(self) -> None:
        self.repo = TransferenciasEntreDepositosRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = TransferenciasEntreDepositos(
                id          = None,
                Repuesto    = row["Repuesto"],
                Año         = row["Año"],
                Cantidad    = row["Cantidad"],
                Cabecera    = row["Cabecera"]
            )
            entities.append(entity)

        self.repo.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        entities = self.repo.get_all()

        data = [
            {
                "id"        : e.id,
                "Repuesto"  : e.Repuesto,
                "Año"       : e.Año,
                "Cantidad"  : e.Cantidad,
                "Cabecera"  : e.Cabecera
            }
            for e in entities
        ]

        return pd.DataFrame(data)

    def get_df_by_cabecera(self, cabecera: str) -> pd.DataFrame:
        entities = self.repo.get_by_cabecera(cabecera)

        data = [
            {
                "id"        : e.id,
                "Repuesto"  : e.Repuesto,
                "Año"       : e.Año,
                "Cantidad"  : e.Cantidad,
                "Cabecera"  : e.Cabecera
            }
            for e in entities
        ]

        return pd.DataFrame(data)