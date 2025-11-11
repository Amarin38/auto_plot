import pandas as pd

from config.constants import PAGE_STRFTIME_YMD
from domain.entities.common.datos_garantias import DatosGarantias
from infrastructure.repositories.common.datos_garantias_repository import DatosGarantiasRepository
from interfaces.viewmodel import ViewModel


class DatosGarantiasVM(ViewModel):
    def __init__(self) -> None:
        self.repo = DatosGarantiasRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = DatosGarantias(
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
            )
            entities.append(entity)

        self.repo.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        entities = self.repo.get_all()

        data = [
            {
                "id": e.id,
                "Año": e.Año,
                "Mes": e.Mes,
                "FechaIngreso"      : e.FechaIngreso,
                "FechaEnvio"        : e.FechaEnvio,
                "Cabecera"          : e.Cabecera,
                "Interno"           : e.Interno,
                "Codigo"            : e.Codigo,
                "Repuesto"          : e.Repuesto,
                "Cantidad"          : e.Cantidad,
                "FechaColocacion"   : e.FechaColocacion,
                "Detalle"           : e.Detalle,
                "Tipo"              : e.Tipo,
                "DiasColocado"      : e.DiasColocado
            }
            for e in entities
        ]

        return pd.DataFrame(data)


    def get_min_date(self) -> str:
        return self.repo.get_min_date().strftime(PAGE_STRFTIME_YMD)


    def get_max_date(self) -> str:
        return self.repo.get_max_date().strftime(PAGE_STRFTIME_YMD)

