from typing import List

import pandas as pd

from config.enums import RepuestoEnum, PeriodoComparacionEnum, CabecerasEnum, ConsumoComparacionRepuestoEnum
from domain.entities.consumo_comparacion import ConsumoComparacion
from infrastructure.repositories.consumo_comparacion_repository import ConsumoComparacionRepository


class ConsumoComparacionVM:
    def __init__(self) -> None:
        self.repo = ConsumoComparacionRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = ConsumoComparacion(
                id              = None,
                Familia         = row["Familia"],
                Articulo        = row["Articulo"],
                Repuesto        = row["Repuesto"],
                TipoRepuesto    = row["TipoRepuesto"],
                Cabecera        = row["Cabecera"],
                Consumo         = row["Consumo"],
                Gasto           = row["Gasto"],
                FechaCompleta   = row["FechaCompleta"],
                PeriodoID       = row["PeriodoID"],
            )
            entities.append(entity)

        self.repo.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        entities = self.repo.get_all()

        return pd.DataFrame(self.get_data(entities))


    def get_df_cabecera_and_tipo_rep_and_periodo(self, cabecera: CabecerasEnum,
                                                       tipo_repuesto: List[ConsumoComparacionRepuestoEnum],
                                                       periodo: List[PeriodoComparacionEnum]) -> pd.DataFrame:
        entities = self.repo.get_by_cabecera_and_tipo_rep_and_periodo(cabecera, tipo_repuesto, periodo)

        return pd.DataFrame(self.get_data(entities))


    @staticmethod
    def get_data(entities) -> list[dict]:
        return [
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
                "PeriodoID"     : e.PeriodoID,
            }
            for e in entities
        ]