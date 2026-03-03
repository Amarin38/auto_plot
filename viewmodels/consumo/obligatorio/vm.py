import pandas as pd

from config.enums import ConsumoObligatorioEnum
from domain.entities.consumo_obligatorio import ConsumoObligatorio
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from interfaces.viewmodel import ViewModel


class ConsumoObligatorioVM(ViewModel):
    def __init__(self, uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()) -> None:
        self.uow = uow

    def save_df(self, df) -> None:
        entities = [
            ConsumoObligatorio(
                id                  = None,
                Cabecera            = row['Cabecera'],
                Repuesto            = row['Repuesto'],
                Año2023             = row['Año2023'],
                Año2024             = row['Año2024'],
                Año2025             = row['Año2025'],
                MinimoAntiguo       = row['MinimoAntiguo'],
                MinimoObligatorio   = row['MinimoObligatorio'],
                UltimaFecha         = row['UltimaFecha'],
            ) for index, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.consumo_obligatorio.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.consumo_obligatorio.get_all()
            return self.get_data(entities) if entities else pd.DataFrame()


    def get_df_repuesto(self, repuesto: ConsumoObligatorioEnum) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.consumo_obligatorio.get_by_repuesto(repuesto)
            return self.get_data(entities) if entities else pd.DataFrame()


    @staticmethod
    def get_data(entities) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "id": e.id,
                    "Cabecera": e.Cabecera,
                    "Repuesto": e.Repuesto,
                    "Año2023": e.Año2023,
                    "Año2024": e.Año2024,
                    "Año2025": e.Año2025,
                    "MinimoAntiguo": e.MinimoAntiguo,
                    "MinimoObligatorio": e.MinimoObligatorio,
                    "UltimaFecha": e.UltimaFecha,
                }
                for e in entities
            ]
        )