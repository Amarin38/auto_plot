import pandas as pd
from pandas import DataFrame

from domain.entities.garantias_consumo import GarantiasConsumo
from infrastructure.repositories.garantias_consumo_repository import GarantiasConsumoRepository


class ConsumoGarantiasVM:
    def __init__(self) -> None:
        self.repo = GarantiasConsumoRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = GarantiasConsumo(
                id                          = None,
                Cabecera                    = row['Cabecera'],
                Repuesto                    = row['Repuesto'],
                TipoRepuesto                = row['TipoRepuesto'],
                Garantia                    = row['Garantia'],
                Transferencia               = row['Transferencia'],
                Total                       = row['Total'],
                PorcentajeTransferencia     = row['PorcentajeTransferencia'],
                PorcentajeGarantia          = row['PorcentajeGarantia'],
            )
            entities.append(entity)

        self.repo.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        entities = self.repo.get_all()
        return self.get_data(entities)


    def get_df_by_tipo_rep_and_cabecera(self, tipo_repuesto: str, cabecera: str) -> pd.DataFrame:
        entities = self.repo.get_by_tipo_rep_and_cabecera(tipo_repuesto, cabecera)
        return self.get_data(entities)


    @staticmethod
    def get_data(entities) -> DataFrame:
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