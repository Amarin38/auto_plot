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

    def save_changes(self, df_original: pd.DataFrame, changes: dict) -> None:
        """
        changes viene de st.session_state["key_del_editor"]
        {
            "edited_rows":  {0: {"RazonSocial": "Nuevo nombre"}, ...},
            "added_rows":   [{"NroProv": 99, "RazonSocial": "...", ...}],
            "deleted_rows": [2, 5]
        }
        """
        with self.uow as uow:
            # Ediciones
            for idx, cols in changes.get("edited_rows", {}).items():
                row = df_original.iloc[idx].to_dict()
                row.update(cols)  # aplicar los cambios encima de la fila original
                entity = Proveedores(
                    NroProv     = int(row["NroProv"]),
                    RazonSocial = row.get("RazonSocial")    or None,
                    CUIT        = row.get("CUIT")           or None,
                    Localidad   = row.get("Localidad")      or None,
                    Mail        = row.get("Mail")           or None,
                    Telefono    = row.get("Telefono")       or None,
                )
                uow.proveedor.update(entity)

            # Nuevas filas
            for row in changes.get("added_rows", []):
                entity = Proveedores(
                    NroProv     = int(row.get("NroProv", 0)),
                    RazonSocial = row.get("RazonSocial"),
                    CUIT        = row.get("CUIT"),
                    Localidad   = row.get("Localidad"),
                    Mail        = row.get("Mail"),
                    Telefono    = row.get("Telefono"),
                )
                uow.proveedor.insert_one(entity)

            # Eliminaciones
            for idx in changes.get("deleted_rows", []):
                nro_prov = int(df_original.iloc[idx]["NroProv"])
                uow.proveedor.delete_by_id(nro_prov)

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