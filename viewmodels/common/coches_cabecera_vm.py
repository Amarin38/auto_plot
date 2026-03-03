import pandas as pd
from pandas import DataFrame

from domain.entities.coches_cabecera import CochesCabecera
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from interfaces.viewmodel import ViewModel


class CochesCabeceraVM(ViewModel):
    def __init__(self, uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()) -> None:
        self.uow = uow


    def save_df(self, df) -> None:
        entities = [
            CochesCabecera(
                id                  = None,
                Cabecera            = row['Cabecera'],
                CochesDuermen       = row['CochesDuermen'],
                CochesDuermenNuevo  = row['CochesDuermenNuevo'],
                CochesSinScania     = row['CochesSinScania'],
            ) for index, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.coches_cabecera.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.coches_cabecera.get_all()
            return self.get_data(entities) if entities else pd.DataFrame()


    @staticmethod
    def get_data(entities) -> DataFrame:
        return pd.DataFrame([
            {
                "id"                    : e.id,
                "Cabecera"              : e.Cabecera,
                "CochesDuermen"         : e.CochesDuermen,
                "CochesDuermenNuevo"    : e.CochesDuermenNuevo,
                "CochesSinScania"       : e.CochesSinScania
            }
            for e in entities
        ])