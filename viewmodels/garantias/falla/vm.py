import pandas as pd

from config.constants_common import PAGE_STRFTIME_YMD
from domain.entities.garantias_consumo import GarantiasConsumo
from domain.entities.garantias_datos import GarantiasDatos
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
            ) for _, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.garantias_falla.insert_many(entities)

    def save_datos_df(self, df) -> None:
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
            ) for _, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.garantias_datos.insert_many(entities)

    def save_consumo_df(self, df) -> None:
        entities = [
            GarantiasConsumo(
                id                      = None,
                Cabecera                = row['Cabecera'],
                Repuesto                = row['Repuesto'],
                TipoRepuesto            = row['TipoRepuesto'],
                Garantia                = row['Garantia'],
                Transferencia           = row['Transferencia'],
                Total                   = row['Total'],
                PorcentajeTransferencia = row['PorcentajeTransferencia'],
                PorcentajeGarantia      = row['PorcentajeGarantia'],
            ) for _, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.garantias_consumo.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.garantias_falla.get_all()
            return self.get_data(entities) if entities else pd.DataFrame()

    def get_datos_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.garantias_datos.get_all()
            return self.get_datos_data(entities) if entities else pd.DataFrame()

    def get_consumo_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.garantias_consumo.get_all()
            return self.get_consumo_data(entities) if entities else pd.DataFrame()


    def get_df_by_tipo_rep_and_cabecera(self, tipo_repuesto: str, cabecera: str) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.garantias_falla.get_by_tipo_rep_and_cabecera(tipo_repuesto, cabecera)
            return self.get_data(entities) if entities else pd.DataFrame()

    def get_consumo_df_by_tipo_rep_and_cabecera(self, tipo_repuesto: str, cabecera: str) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.garantias_consumo.get_by_tipo_rep_and_cabecera(tipo_repuesto, cabecera)
            return self.get_consumo_data(entities) if entities else pd.DataFrame()


    def get_datos_min_date(self) -> str:
        with self.uow as uow:
            return uow.garantias_datos.get_min_date().strftime(PAGE_STRFTIME_YMD)

    def get_datos_max_date(self) -> str:
        with self.uow as uow:
            return uow.garantias_datos.get_max_date().strftime(PAGE_STRFTIME_YMD)


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

    @staticmethod
    def get_datos_data(entities) -> pd.DataFrame:
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

    @staticmethod
    def get_consumo_data(entities) -> pd.DataFrame:
        return pd.DataFrame([
            {
                "id": e.id,
                "Cabecera": e.Cabecera,
                "Repuesto": e.Repuesto,
                "TipoRepuesto": e.TipoRepuesto,
                "Garantia": e.Garantia,
                "Transferencia": e.Transferencia,
                "Total": e.Total,
                "PorcentajeTransferencia": e.PorcentajeTransferencia,
                "PorcentajeGarantia": e.PorcentajeGarantia
            }
            for e in entities
        ])