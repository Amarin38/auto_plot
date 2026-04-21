import numpy as np
import pandas as pd

from domain.entities.datos_repuestos_codigos import RepuestosCodigos, RepuestosCodigosFiltro
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from interfaces.viewmodel import ViewModel


class RepuestosCodigosVM(ViewModel):
    def __init__(self, uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()) -> None:
        self.uow = uow

    @staticmethod
    def formatear_df(df: pd.DataFrame):
        df = df.rename(columns={"Articulo":"Descripcion", "Codigo":"Codigos"})

        df[["Familia", "Articulo"]] = df["Codigos"].str.strip().str.split(".", expand=True)

        familia = df["Familia"].str.zfill(3)
        articulo = df["Articulo"].str.zfill(5)
        df["CodigosConCero"] = familia.str.cat(articulo, sep=".")

        df = df[["Descripcion", "Deposito", "Familia", "Articulo", "Codigos", "CodigosConCero"]]
        return df


    def save_df(self, df: pd.DataFrame) -> None:
        df = self.formatear_df(df)

        entities = [
            RepuestosCodigos(
                id              = None,
                Descripcion     = row['Descripcion'],
                Deposito        = row['Deposito'],
                Familia         = row['Familia'],
                Articulo        = row['Articulo'],
                Codigos         = row['Codigos'],
                CodigosConCero  = row['CodigosConCero']
            ) for index, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.repuestos_codigos.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.repuestos_codigos.get_all()
            return self.get_data(entities) if entities else pd.DataFrame()


    def get_by_args(self, rep_cod_filtros: RepuestosCodigosFiltro):
        with self.uow as uow:
            df_base = self.get_data(uow.repuestos_codigos.get_all())

        if df_base.empty:
            return pd.DataFrame()

        mask = np.ones(len(df_base), dtype=bool)

        if rep_cod_filtros.Descripcion:
            mask &= df_base["Descripcion"].str.contains(rep_cod_filtros.Descripcion)

        if rep_cod_filtros.Deposito:
            mask &= df_base["Deposito"].isin(rep_cod_filtros.Deposito)

        if rep_cod_filtros.CodigosConCero:
            mask &= df_base["CodigosConCero"].str.startswith(rep_cod_filtros.CodigosConCero)

        return df_base[mask]


    @staticmethod
    def get_data(entities) -> pd.DataFrame:
        return pd.DataFrame([
            {
                "id"                : e.id,
                "Descripcion"       : e.Descripcion,
                "Deposito"          : e.Deposito,
                "Familia"           : e.Familia,
                "Articulo"          : e.Articulo,
                "Codigos"           : e.Codigos,
                "CodigosConCero"    : e.CodigosConCero
            }
            for e in entities
        ])