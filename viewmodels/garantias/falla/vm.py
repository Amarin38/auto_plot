import pandas as pd

from domain.entities.garantias_falla import GarantiasFalla
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork


class FallaGarantiasVM:
    def __init__(self, uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()) -> None:
        self.uow = uow

    def save_df(self, df) -> None:
        entities = [
            GarantiasFalla(
                id                  = None,
                Cabecera            = row['Cabecera'],
                Repuesto            = row['Repuesto'],
                TipoRepuesto        = row['TipoRepuesto'],
                PromedioTiempoFalla = row['PromedioTiempoFalla'],
            ) for index, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.garantias_falla.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.garantias_falla.get_all()
            return self.get_data(entities) if entities else pd.DataFrame()


    def get_df_by_tipo_rep_and_cabecera(self, tipo_repuesto: str, cabecera: str) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.garantias_falla.get_by_tipo_rep_and_cabecera(tipo_repuesto, cabecera)
            return self.get_data(entities) if entities else pd.DataFrame()


    @staticmethod
    def get_data(entities) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "id": e.id,
                    "Cabecera": e.Cabecera,
                    "Repuesto": e.Repuesto,
                    "TipoRepuesto": e.TipoRepuesto,
                    "PromedioTiempoFalla": e.PromedioTiempoFalla
                }
                for e in entities
            ]
        )