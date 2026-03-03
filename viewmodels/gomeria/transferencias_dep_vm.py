import pandas as pd

from domain.entities.gomeria_transferencias_dep import GomeriaTransferenciasEntreDep
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from interfaces.viewmodel import ViewModel


class TransferenciasEntreDepositosVM(ViewModel):
    def __init__(self, uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()) -> None:
        self.uow = uow


    def save_df(self, df) -> None:
        entities = [
            GomeriaTransferenciasEntreDep(
                id          = None,
                Repuesto    = row["Repuesto"],
                Año         = row["Año"],
                Cantidad    = row["Cantidad"],
                Cabecera    = row["Cabecera"]
            ) for index, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.gomeria_transferencias.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.gomeria_transferencias.get_all()
            return self.get_data(entities) if entities else pd.DataFrame()


    def get_df_by_cabecera(self, cabecera: str) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.gomeria_transferencias.get_by_cabecera(cabecera)
            return self.get_data(entities) if entities else pd.DataFrame()


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