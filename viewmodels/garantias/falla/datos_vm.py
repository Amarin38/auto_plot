import pandas as pd

from config.constants_common import PAGE_STRFTIME_YMD
from domain.entities.garantias_datos import GarantiasDatos
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from interfaces.viewmodel import ViewModel


class DatosGarantiasVM(ViewModel):
    def __init__(self, uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()) -> None:
        self.uow = uow

    def save_df(self, df) -> None:
        entities = [
            GarantiasDatos(
                id              = None,
                Año             = row['Año'],
                Mes             = row['Mes'],
                FechaIngreso    = row['FechaIngreso'],
                FechaEnvio      = row['FechaEnvio'],
                Cabecera        = row['Cabecera'],
                Interno         = row['Interno'],
                Codigo          = row['Codigo'],
                Repuesto        = row['Repuesto'],
                Cantidad        = row['Cantidad'],
                FechaColocacion = row['FechaColocacion'],
                Detalle         = row['Detalle'],
                Tipo            = row['Tipo'],
                DiasColocado    = row['DiasColocado'],
            ) for index, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.garantias_datos.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.garantias_datos.get_all()
            return self.get_data(entities) if entities else pd.DataFrame()


    def get_min_date(self) -> str:
        with self.uow as uow:
            return uow.garantias_datos.get_min_date().strftime(PAGE_STRFTIME_YMD)


    def get_max_date(self) -> str:
        with self.uow as uow:
            return uow.garantias_datos.get_max_date().strftime(PAGE_STRFTIME_YMD)


    @staticmethod
    def get_data(entities) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "id": e.id,
                    "Año": e.Año,
                    "Mes": e.Mes,
                    "FechaIngreso": e.FechaIngreso,
                    "FechaEnvio": e.FechaEnvio,
                    "Cabecera": e.Cabecera,
                    "Interno": e.Interno,
                    "Codigo": e.Codigo,
                    "Repuesto": e.Repuesto,
                    "Cantidad": e.Cantidad,
                    "FechaColocacion": e.FechaColocacion,
                    "Detalle": e.Detalle,
                    "Tipo": e.Tipo,
                    "DiasColocado": e.DiasColocado
                }
                for e in entities
            ]
        )
