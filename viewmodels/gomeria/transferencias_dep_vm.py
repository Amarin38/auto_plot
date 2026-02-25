import pandas as pd

from domain.entities.gomeria_transferencias_dep import GomeriaTransferenciasEntreDep
from infrastructure.repositories.gomeria_transferencias_dep_repository import \
    GomeriaTransferenciasEntreDepRepository
from interfaces.viewmodel import ViewModel


class TransferenciasEntreDepositosVM(ViewModel):
    def __init__(self) -> None:
        self.repo = GomeriaTransferenciasEntreDepRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = GomeriaTransferenciasEntreDep(
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
        return self.get_data(entities)

    def get_df_by_cabecera(self, cabecera: str) -> pd.DataFrame:
        entities = self.repo.get_by_cabecera(cabecera)
        return self.get_data(entities)


    @staticmethod
    def get_data(entities) -> pd.DataFrame:
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