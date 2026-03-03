import pandas as pd

from config.enums import RepuestoEnum
from domain.entities.consumo_historial import ConsumoHistorial
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork


class HistorialConsumoVM:
    def __init__(self, uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()) -> None:
        self.uow = uow

    def save_df(self, df) -> None:
        entities = [
            ConsumoHistorial(
                id           = None,
                TipoRepuesto = row['TipoRepuesto'],
                Año          = row['Año'],
                TotalConsumo = row['TotalConsumo'],
                FechaMin     = row['FechaMin'],
                FechaMax     = row['FechaMax'],
            ) for index, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.consumo_historial.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.consumo_historial.get_all()
            return self.get_data(entities) if entities else pd.DataFrame()


    def get_df_tipo_repuesto(self, tipo_repuesto: RepuestoEnum) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.consumo_historial.get_by_tipo_rep(tipo_repuesto)
            return self.get_data(entities) if entities else pd.DataFrame()


    @staticmethod
    def get_data(entities) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "id": e.id,
                    "TipoRepuesto": e.TipoRepuesto,
                    "Año": e.Año,
                    "TotalConsumo": e.TotalConsumo,
                    "FechaMin": e.FechaMin,
                    "FechaMax": e.FechaMax,
                }
                for e in entities
            ]
        )