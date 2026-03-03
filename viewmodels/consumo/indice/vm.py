import pandas as pd

from domain.entities.consumo_indice import ConsumoIndice
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork

class IndiceConsumoVM:
    def __init__(self, uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()) -> None:
        self.uow = uow


    def save_df(self, df) -> None:
        entities = [
            ConsumoIndice(
                id              = None,
                Cabecera        = row['Cabecera'],
                Repuesto        = row['Repuesto'],
                TipoRepuesto    = row['TipoRepuesto'],
                TotalConsumo    = row['TotalConsumo'],
                TotalCoste      = row['TotalCoste'],
                IndiceConsumo   = row['ConsumoIndice'],
                UltimaFecha     = row['UltimaFecha'],
                TipoOperacion   = row['TipoOperacion'],
            ) for index, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.consumo_indice.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.consumo_indice.get_all()
            return self.get_data(entities) if entities else pd.DataFrame()


    def get_df_tipo_repuesto_and_tipo_indice(self, tipo_repuesto: str, tipo_indice: str) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.consumo_indice.get_by_tipo_rep_and_tipo_indice(tipo_repuesto, tipo_indice)
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
                    "TotalConsumo": e.TotalConsumo,
                    "ConsumoIndice": e.IndiceConsumo,
                    "UltimaFecha": e.UltimaFecha,
                    "TipoOperacion": e.TipoOperacion,
                }
                for e in entities
            ]
        )
