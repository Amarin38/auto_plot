import numpy as np
import pandas as pd

from domain.entities.datos_proveedores import Proveedores
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from interfaces.viewmodel import ViewModel


class ProveedoresVM(ViewModel):
    def __init__(self, uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()) -> None:
        self.uow = uow


    def save_df(self, df: pd.DataFrame) -> None:
        df = df.rename(columns={"Nro prov": "NroProv", "Razon social": "RazonSocial", "Cuit": "CUIT"})
        df["NroProv"] = df["NroProv"].astype("int64")
        df["Telefono"] = df["Telefono"].astype(str).replace("nan", None)

        entities = [
            Proveedores(
                NroProv             = row['NroProv'],
                RazonSocial         = row['RazonSocial'],
                CUIT                = row['CUIT'],
                Localidad           = row['Localidad'],
                Mail                = row['Mail'],
                Telefono            = row['Telefono']
            ) for index, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.proveedor.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.proveedor.get_all()
            return self.get_data(entities) if entities else pd.DataFrame()


    def get_by_args(self, proveedores_filtros):
        with self.uow as uow:
            df_base = self.get_data(uow.proveedor.get_all())

        if df_base.empty:
            return pd.DataFrame()

        mask = np.ones(len(df_base), dtype=bool)

        if proveedores_filtros.NroProv:
            df_base["NroProv"] = df_base["NroProv"].astype(str)
            mask &= df_base["NroProv"].str.startswith(proveedores_filtros.NroProv.strip())

        if proveedores_filtros.RazonSocial:
            mask &= df_base["RazonSocial"].str.contains(proveedores_filtros.RazonSocial.upper().strip())

        if proveedores_filtros.CUIT:
            mask &= df_base["CUIT"].str.contains(proveedores_filtros.CUIT.strip())

        if proveedores_filtros.Localidad:
            mask &= df_base["Localidad"].isin(proveedores_filtros.Localidad)

        if proveedores_filtros.Mail:
            mask &= df_base["Mail"].str.contains(proveedores_filtros.Mail.strip())

        if proveedores_filtros.Telefono:
            mask &= df_base["Telefono"].str.contains(proveedores_filtros.Telefono.strip())

        return df_base[mask]


    def backup_google_sheet(self, df_viejo: pd.DataFrame, df_nuevo: pd.DataFrame) -> None:
        """ Compara los cambios entre el DF de la google sheet y la guardada en la base de datos y hace una copia."""
        idx_comunes = df_viejo.index.intersection(df_nuevo.index)

        df_viejo_comun = df_viejo.loc[idx_comunes].astype(str).replace("nan", "")
        df_nuevo_comun = df_nuevo.loc[idx_comunes].astype(str).replace("nan", "")

        mascara_cambios = (df_viejo_comun != df_nuevo_comun).any(axis=1)
        idx_editados = idx_comunes[mascara_cambios]
        idx_nuevos = df_nuevo.index.difference(df_viejo.index)

        with self.uow as uow:
            for idx in idx_editados:
                row = df_nuevo.loc[idx]
                entity = Proveedores(
                    NroProv     = int(row["NroProv"]),
                    RazonSocial = row.get("RazonSocial")    if pd.notna(row.get("RazonSocial")) else None,
                    CUIT        = row.get("CUIT")           if pd.notna(row.get("CUIT")) else None,
                    Localidad   = row.get("Localidad")      if pd.notna(row.get("Localidad")) else None,
                    Mail        = row.get("Mail")           if pd.notna(row.get("Mail")) else None,
                    Telefono    = row.get("Telefono")       if pd.notna(row.get("Telefono")) else None
                )
                uow.proveedor.update(entity)

            for idx in idx_nuevos:
                row = df_nuevo.loc[idx]
                entity = Proveedores(
                    NroProv     = int(row.get("NroProv", 0)),
                    RazonSocial = row.get("RazonSocial")    if pd.notna(row.get("RazonSocial")) else None,
                    CUIT        = row.get("CUIT")           if pd.notna(row.get("CUIT")) else None,
                    Localidad   = row.get("Localidad")      if pd.notna(row.get("Localidad")) else None,
                    Mail        = row.get("Mail")           if pd.notna(row.get("Mail")) else None,
                    Telefono    = row.get("Telefono")       if pd.notna(row.get("Telefono")) else None
                )
                uow.proveedor.insert_one(entity)


    @staticmethod
    def get_data(entities) -> pd.DataFrame:
        return pd.DataFrame([
            {
                "NroProv"       : e.NroProv,
                "RazonSocial"   : e.RazonSocial,
                "CUIT"          : e.CUIT,
                "Localidad"     : e.Localidad,
                "Mail"          : e.Mail,
                "Telefono"      : e.Telefono
            }
            for e in entities
        ])