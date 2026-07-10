from datetime import date

import pandas as pd
import streamlit

from config.constants_common import PARQUE_MOVIL_COLS, PARQUE_MOVIL_COLS_TYPE, REPUESTOS_CODIGOS_COLS_RENAME
from domain.entities.datos.coches_cabecera import CochesCabecera
from domain.entities.datos.maximos_minimos import MaximosMinimos
from domain.entities.datos.proveedores import Proveedores
from domain.entities.datos.repuestos_codigos import RepuestosCodigos
from domain.entities.datos.usuarios_codigos import UsuariosCodigos
from domain.entities.datos.json_config import JSONConfig
from domain.entities.parque_movil.PARQUE_MOVIL import ParqueMovil
from viewmodels.base_vm import BaseVM


class CochesCabeceraVM(BaseVM[CochesCabecera]):
    def __init__(self) -> None:
        columns_df = list(CochesCabecera.model_fields.keys())
        super().__init__(CochesCabecera, "coches_cabecera", columns_df)


class MaximosMinimosVM(BaseVM[MaximosMinimos]):
    def __init__(self) -> None:
        columns_df = list(MaximosMinimos.model_fields.keys())
        super().__init__(MaximosMinimos, "maximos_minimos", columns_df)


class ProveedoresVM(BaseVM[Proveedores]):
    def __init__(self) -> None:
        columns_df = list(Proveedores.model_fields.keys())
        super().__init__(Proveedores, "proveedor", columns_df)


class RepuestosCodigosVM(BaseVM[RepuestosCodigos]):
    def __init__(self) -> None:
        columns_df = list(RepuestosCodigos.model_fields.keys())
        super().__init__(RepuestosCodigos, "repuestos_codigos", columns_df)


    @staticmethod
    def formatear_df(df: pd.DataFrame):
        df = df.rename(columns=REPUESTOS_CODIGOS_COLS_RENAME)
        df[["Familia", "Articulo"]] = df["Codigos"].str.strip().str.split(".", expand=True)

        familia = df["Familia"].str.zfill(3)
        articulo = df["Articulo"].str.zfill(5)
        df["CodigosConCero"] = familia.str.cat(articulo, sep=".")

        return df


class UsuariosCodigosVM(BaseVM[UsuariosCodigos]):
    def __init__(self) -> None:
        columns_df = list(UsuariosCodigos.model_fields.keys())
        super().__init__(UsuariosCodigos, "usuarios_codigos", columns_df)

    def get_df_by_usuario_antiguo(self, usuario_antiguo: str) -> pd.DataFrame:
        return self.get_df_by_filters({"UsuariosAntiguos": usuario_antiguo})


    def get_df_by_usuario_nuevo(self, usuario_nuevo: str) -> pd.DataFrame:
        return self.get_df_by_filters({"UsuariosNuevos": usuario_nuevo})


class JSONConfigVM(BaseVM[JSONConfig]):
    def __init__(self) -> None:
        columns_df = list(JSONConfig.model_fields.keys())
        super().__init__(JSONConfig, "json_config", columns_df)


    def get_df_by_name(self, nombre: str):
        df = self.get_df_by_filters({"nombre": nombre})
        return df["data"].iloc[0]


class ParqueMovilVM(BaseVM[ParqueMovil]):
    def __init__(self) -> None:
        columns_df = list(ParqueMovil.model_fields.keys())
        super().__init__(ParqueMovil, "parque_movil", columns_df)


    @streamlit.cache_data(ttl=3600, show_spinner="Consultando a la base de datos...", show_time=True)
    def get_by_fechas(_self, fecha_desde: date, fecha_hasta: date) -> pd.DataFrame:
        df_fechas = _self.get_df_between_dates("FechaParqueMovil", fecha_desde, fecha_hasta)

        rows = ((
            e.id, e.FechaParqueMovil, e.Linea, e.Interno, e.Dominio, e.Asientos,
            e.Año, e.ChasisMarca, e.ChasisModelo, e.ChasisNum, e.MotorMarca,
            e.MotorModelo, e.MotorNum, e.Carroceria
        ) for e in df_fechas)

        df = pd.DataFrame.from_records(rows, columns=PARQUE_MOVIL_COLS)
        valores_na = {"Linea": 0, "Interno": 0, "Dominio": "", "Asientos": 0, "Año": 0,
                      "ChasisMarca": "", "ChasisModelo": "", "ChasisNum": "",
                      "MotorMarca": "", "MotorModelo": "", "MotorNum": "", "Carroceria": ""}

        df = df.fillna(value=valores_na).astype(PARQUE_MOVIL_COLS_TYPE)

        if df.empty:
            return pd.DataFrame()

        return pd.DataFrame(df)



