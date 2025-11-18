import pandas as pd

from config.enums import ConsumoObligatorioEnum
from domain.entities.consumo_obligatorio import ConsumoObligatorio
from infrastructure.repositories.consumo_obligatorio_repository import ConsumoObligatorioRepository
from interfaces.viewmodel import ViewModel


class ConsumoObligatorioVM(ViewModel):
    def __init__(self) -> None:
        self.repo = ConsumoObligatorioRepository()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = ConsumoObligatorio(
                id                  = None,
                Cabecera            = row['Cabecera'],
                Repuesto            = row['Repuesto'],
                Año2023             = row['Año2023'],
                Año2024             = row['Año2024'],
                Año2025             = row['Año2025'],
                MinimoObligatorio   = row['MinimoObligatorio'],
                UltimaFecha         = row['UltimaFecha'],
            )
            entities.append(entity)

        self.repo.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        entities = self.repo.get_all()

        data = [
            {
                "id"                    : e.id,
                "Cabecera"              : e.Cabecera,
                "Repuesto"              : e.Repuesto,
                "Año2023"               : e.Año2023,
                "Año2024"               : e.Año2024,
                "Año2025"               : e.Año2025,
                "MinimoObligatorio"     : e.MinimoObligatorio,
                "UltimaFecha"           : e.UltimaFecha,
            }
            for e in entities
        ]

        return pd.DataFrame(data)


    def get_df_repuesto(self, repuesto: ConsumoObligatorioEnum) -> pd.DataFrame:
        entity = self.repo.get_by_repuesto(repuesto)

        data = [
            {
                "id"                    : e.id,
                "Cabecera"              : e.Cabecera,
                "Repuesto"              : e.Repuesto,
                "Año2023"               : e.Año2023,
                "Año2024"               : e.Año2024,
                "Año2025"               : e.Año2025,
                "MinimoObligatorio"     : e.MinimoObligatorio,
                "UltimaFecha"           : e.UltimaFecha,
            }
            for e in entity
        ]

        return pd.DataFrame(data)