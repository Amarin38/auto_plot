import pandas as pd

from domain.entities.services.consumo_garantias import ConsumoGarantias
from infrastructure.repositories.services.consumo_garantias_repository import ConsumoGarantiasRepository


class ConsumoGarantiasVM:
    def __init__(self) -> None:
        self.repo = ConsumoGarantiasRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = ConsumoGarantias(
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

        data = [
            {
                "id"                        : e.id,
                "Cabecera"                  : e.Cabecera,
                "Repuesto"                  : e.Repuesto,
                "TipoRepuesto"              : e.TipoRepuesto,
                "Garantia"                  : e.Garantia,
                "Transferencia"             : e.Transferencia,
                "Total"                     : e.Total,
                "PorcentajeTransferencia"   : e.PorcentajeTransferencia,
                "PorcentajeGarantia"        : e.PorcentajeGarantia
            }
            for e in entities
        ]

        return pd.DataFrame(data)


    def get_df_by_tipo_rep_and_cabecera(self, tipo_repuesto: str, cabecera: str) -> pd.DataFrame:
        entities = self.repo.get_by_tipo_rep_and_cabecera(tipo_repuesto, cabecera)

        data = [
            {
                "id"                        : e.id,
                "Cabecera"                  : e.Cabecera,
                "Repuesto"                  : e.Repuesto,
                "TipoRepuesto"              : e.TipoRepuesto,
                "Garantia"                  : e.Garantia,
                "Transferencia"             : e.Transferencia,
                "Total"                     : e.Total,
                "PorcentajeTransferencia"   : e.PorcentajeTransferencia,
                "PorcentajeGarantia"        : e.PorcentajeGarantia
            }
            for e in entities
        ]

        return pd.DataFrame(data)