import pandas as pd

from domain.entities.consumo_desviacion_indices import ConsumoDesviacionIndices
from infrastructure.repositories.consumo_desviacion_indices_repository import ConsumoDesviacionIndicesRepository


class DesviacionIndicesVM:
    def __init__(self) -> None:
        self.repo = ConsumoDesviacionIndicesRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = ConsumoDesviacionIndices(
                id                  = None,
                Cabecera            = row['Cabecera'],
                MediaCabecera       = row['MediaCabecera'],
                MediaDeMedias       = row['MediaDeMedias'],
                Diferencia          = row['Diferencia'],
                Desviacion          = row['Desviacion'],
                DesviacionPor       = row['DesviacionPor'],
                FechaCompleta       = row['FechaCompleta']
            )
            entities.append(entity)

        self.repo.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        entities = self.repo.get_all()

        data = [
            {
                "id"            : e.id,
                "Cabecera"      : e.Cabecera,
                "MediaCabecera" : e.MediaCabecera,
                "MediaDeMedias" : e.MediaDeMedias,
                "Diferencia"    : e.Diferencia,
                "Desviacion"    : e.Desviacion,
                "DesviacionPor" : e.DesviacionPor,
                "FechaCompleta" : e.FechaCompleta
            }
            for e in entities
        ]

        return pd.DataFrame(data)