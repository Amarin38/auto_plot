import pandas as pd

from domain.entities.distribucion_normal import DistribucionNormal
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from interfaces.viewmodel import ViewModel


class DistribucionNormalVM(ViewModel):
    def __init__(self, uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()) -> None:
        self.uow = uow

    def save_df(self, df) -> None:
        entities = [
            DistribucionNormal(
                id                  = None,
                Años                = row['Años'],
                Cambio              = row['Cambio'],
                Cabecera            = row['Cabecera'],
                Repuesto            = row['Repuesto'],
                TipoRepuesto        = row['TipoRepuesto'],
                AñoPromedio         = row['AñoPromedio'],
                DesviacionEstandar  = row['DesviacionEstandar'],
                DistribucionNormal  = row['DistribucionNormal'],
            ) for index, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.distribucion_normal.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.distribucion_normal.get_all()
            return self.get_data(entities) if entities else pd.DataFrame()


    def get_df_by_repuesto(self, repuesto: str) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.distribucion_normal.get_by_repuesto(repuesto)
            return self.get_data(entities) if entities else pd.DataFrame()


    @staticmethod
    def get_data(entities) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "id": e.id,
                    "Años": e.Años,
                    "Cambio": e.Cambio,
                    "Cabecera": e.Cabecera,
                    "Repuesto": e.Repuesto,
                    "TipoRepuesto": e.TipoRepuesto,
                    "AñoPromedio": e.AñoPromedio,
                    "DesviacionEstandar": e.DesviacionEstandar,
                    "DistribucionNormal": e.DistribucionNormal
                }
                for e in entities
            ]
        )