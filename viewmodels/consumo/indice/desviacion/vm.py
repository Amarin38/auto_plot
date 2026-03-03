import pandas as pd

from config.enums import RepuestoEnum
from domain.entities.consumo_desviacion_indices import ConsumoDesviacionIndices
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork


class DesviacionIndicesVM:
    def __init__(self, uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()) -> None:
        self.uow = uow


    def save_df(self, df) -> None:
        entities = [
            ConsumoDesviacionIndices(
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
            ) for index, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.consumo_desviacion_indices.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.consumo_desviacion_indices.get_all()
            return self.get_data(entities) if entities else pd.DataFrame()


    def get_df_by_tipo_rep(self, tipo_rep: RepuestoEnum) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.consumo_desviacion_indices.get_by_tipo_rep(tipo_rep)
            return self.get_data(entities) if entities else pd.DataFrame()


    def delete_all(self) -> None:
        with self.uow as uow:
            uow.consumo_desviacion_indices.delete()


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