import pandas as pd

from config.enums import RepuestoEnum
from domain.entities.consumo_desviacion_indices import ConsumoDesviacionIndices
from infrastructure.repositories.consumo_desviacion_indices_repository import ConsumoDesviacionIndicesRepository


class DesviacionIndicesVM:
    def __init__(self) -> None:
        self.repo = ConsumoDesviacionIndicesRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = ConsumoDesviacionIndices(
                id                      = None,
                Cabecera                = row['Cabecera'],
                TipoRepuesto            = row['TipoRepuesto'],
                MediaRepuesto           = row['MediaRepuesto'],
                MediaDeMediasRepuesto   = row['MediaDeMediasRepuesto'],
                DiferenciaRepuesto      = row['DiferenciaRepuesto'],
                DesviacionRepuesto      = row['DesviacionRepuesto'],
                DesviacionRepuestoPor   = row['DesviacionRepuestoPor'],
                MediaCabecera           = row['MediaCabecera'],
                MediaDeMediasCabecera   = row['MediaDeMediasCabecera'],
                DiferenciaCabecera      = row['DiferenciaCabecera'],
                DesviacionCabecera      = row['DesviacionCabecera'],
                DesviacionCabeceraPor   = row['DesviacionCabeceraPor'],
                FechaCompleta           = row['FechaCompleta']
            )
            entities.append(entity)

        self.repo.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        entities = self.repo.get_all()
        return self.get_data(entities)


    def get_df_by_tipo_rep(self, tipo_rep: RepuestoEnum) -> pd.DataFrame:
        entities = self.repo.get_by_tipo_rep(tipo_rep)
        return self.get_data(entities)


    def delete_all(self) -> None:
        self.repo.delete()


    @staticmethod
    def get_data(entities) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "id": e.id,
                    "Cabecera": e.Cabecera,
                    "TipoRepuesto": e.TipoRepuesto,
                    "MediaCabecera": e.MediaRepuesto,
                    "MediaDeMedias": e.MediaDeMediasRepuesto,
                    "Diferencia": e.DiferenciaRepuesto,
                    "Desviacion": e.DesviacionRepuesto,
                    "DesviacionPor": e.DesviacionRepuestoPor,
                    "FechaCompleta": e.FechaCompleta
                }
                for e in entities
            ]
        )