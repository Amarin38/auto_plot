import pandas as pd

from domain.entities.consumo_indice import ConsumoIndice
from infrastructure.repositories.consumo_indice_repository import ConsumoIndiceRepository


class IndiceConsumoVM:
    def __init__(self) -> None:
        self.repo = ConsumoIndiceRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = ConsumoIndice(
                id              = None,
                Cabecera        = row['Cabecera'],
                Repuesto        = row['Repuesto'],
                TipoRepuesto    = row['TipoRepuesto'],
                TotalConsumo    = row['TotalConsumo'],
                TotalCoste      = row['TotalCoste'],
                IndiceConsumo   = row['ConsumoIndice'],
                UltimaFecha     = row['UltimaFecha'],
                TipoOperacion   = row['TipoOperacion'],
            )
            entities.append(entity)

        self.repo.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        entities = self.repo.get_all()

        data = [
            {
                "id"            : e.id,
                "Cabecera"      : e.Cabecera,
                "Repuesto"      : e.Repuesto,
                "TipoRepuesto"  : e.TipoRepuesto,
                "TotalConsumo"  : e.TotalConsumo,
                "ConsumoIndice" : e.IndiceConsumo,
                "UltimaFecha"   : e.UltimaFecha,
                "TipoOperacion" : e.TipoOperacion,
            }
            for e in entities
        ]

        return pd.DataFrame(data)


    def get_df_tipo_repuesto_and_tipo_indice(self, tipo_repuesto: str, tipo_indice: str) -> pd.DataFrame:
        entities = self.repo.get_by_tipo_rep_and_tipo_indice(tipo_repuesto, tipo_indice)

        data = [
            {
                "id"            : e.id,
                "Cabecera"      : e.Cabecera,
                "Repuesto"      : e.Repuesto,
                "TipoRepuesto"  : e.TipoRepuesto,
                "TotalConsumo"  : e.TotalConsumo,
                "ConsumoIndice" : e.IndiceConsumo,
                "UltimaFecha"   : e.UltimaFecha,
                "TipoOperacion" : e.TipoOperacion,
            }
            for e in entities
        ]

        return pd.DataFrame(data)