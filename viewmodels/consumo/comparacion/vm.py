from typing import List

import pandas as pd

from config.enums import PeriodoComparacionEnum, CabecerasEnum, ConsumoComparacionRepuestoEnum
from domain.entities.consumo_comparacion import ConsumoComparacion
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork


class ConsumoComparacionVM:
    def __init__(self, uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()) -> None:
        self.uow = uow

    def save_df(self, df) -> None:
        entities = [
            ConsumoComparacion(
                id              = None,
                Familia         = row["Familia"],
                Articulo        = row["Articulo"],
                Repuesto        = row["Repuesto"],
                TipoRepuesto    = row["TipoRepuesto"],
                Cabecera        = row["Cabecera"],
                Consumo         = row["Consumo"],
                Gasto           = row["Gasto"],
                FechaCompleta   = row["FechaCompleta"],
                FechaTitulo     = row["FechaTitulo"],
                PeriodoID       = row["PeriodoID"],
            ) for _, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.consumo_comparacion.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.consumo_comparacion.get_all()
            return self.get_data(entities) if entities else pd.DataFrame()


    def get_df_cabecera_and_tipo_rep_and_periodo(self, cabecera: CabecerasEnum,
                                                       tipo_repuesto: List[ConsumoComparacionRepuestoEnum],
                                                       periodo: List[PeriodoComparacionEnum]) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.consumo_comparacion.get_by_cabecera_and_tipo_rep_and_periodo(cabecera, tipo_repuesto, periodo)
            return self.get_data(entities) if entities else pd.DataFrame()


    @staticmethod
    def get_data(entities) -> pd.DataFrame:
        return pd.DataFrame([
            {
                "id"            : e.id,
                "Familia"       : e.Familia,
                "Articulo"      : e.Articulo,
                "Repuesto"      : e.Repuesto,
                "TipoRepuesto"  : e.TipoRepuesto,
                "Cabecera"      : e.Cabecera,
                "Consumo"       : e.Consumo,
                "Gasto"         : e.Gasto,
                "FechaCompleta" : e.FechaCompleta,
                "FechaTitulo"   : e.FechaTitulo,
                "PeriodoID"     : e.PeriodoID,
            }
            for e in entities
        ])