from typing import Union, List, Tuple

import pandas as pd

from config.constants_common import VACIO_FECHA, DEL_COLUMNS_MOVNOM, DEL_COLUMNS_FICMOV, INTERNOS_DEVOLUCION, \
                                    MOV_SALIDAS_LIST, MOV_ENTRADAS_LIST, MOV_DEVOLUCIONES_LIST, MOV_TRANSFERENCIAS_LIST
from config.enums import MovimientoEnum
from utils.common_utils import CommonUtils
from utils.exception_utils import execute_safely


class InventoryDataCleaner:
    def __init__(self):
        self.common = CommonUtils()


    def run_all(self, df_directory: list, tipo: MovimientoEnum)-> pd.DataFrame:
        """
        Arregla el listado de existencias de la siguiente forma:
        - Transforma todos los xls a xlsx.
        - Concatena todos los archivos en uno solo.
        - Elimina las columns innecesarias.
        - Filtra por salida.
        """
        df: pd.DataFrame = self.common.concat_dataframes(df_directory)

        if df.empty:
            return pd.DataFrame()

        try:
            df = self.common.delete_by_content(df, "ficfec", [VACIO_FECHA])
        except (KeyError, IndexError):
            df = self.common.delete_by_content(df, "FechaCompleta", [VACIO_FECHA])

        df = self._transform(df, tipo)
        df = self.common.delete_unnamed_cols(df)

        return self.filter_mov(df, tipo)


    @execute_safely
    def _transform(self, df: pd.DataFrame, tipo: MovimientoEnum) -> pd.DataFrame:
        # transformo las columnas para poder eliminarlas
        df.columns = df.columns.str.strip("'").str.strip()
        df.columns = [
            (col.decode('utf8', 'ignore')
            if isinstance(col, bytes) else col)
            for col in df.columns
        ] # paso a utf-8

        df_updated = self.common.update_columns(df, "columns") # renombro columnas

        match tipo:
            case MovimientoEnum.SALIDAS: df_updated = df_updated.drop(columns=DEL_COLUMNS_MOVNOM, axis=1, errors="ignore")
            case MovimientoEnum.TRANSFERENCIAS: df_updated = df_updated.drop(columns=DEL_COLUMNS_FICMOV, axis=1, errors="ignore")

        df_updated = self.common.update_rows_by_dict(df_updated, "depositos", "Cabecera")

        return df_updated


    @execute_safely
    def filter(self, df: pd.DataFrame, column: str, filter_args: str, filter_type: str):
        filtered_df = pd.DataFrame()

        match filter_type:
            case "contains": filtered_df = df.loc[df[column].str.contains(filter_args, na=False)] 
            case "startswith": filtered_df = df.loc[df[column].str.startswith(filter_args, na=False)]

        filtered_df = self.common.delete_unnamed_cols(filtered_df)

        return filtered_df
    

    @execute_safely
    def filter_codigo(self, df: pd.DataFrame, filter_args: float) -> pd.DataFrame:
        filtered_df = df.loc[df["Codigo"] == filter_args]
        filtered_df = self.common.delete_unnamed_cols(filtered_df)

        return filtered_df
        
    
    @execute_safely
    def filter_lista_codigos(self, df: pd.DataFrame, filter_args: Union[List, Tuple]) -> pd.DataFrame:
        """ 
        Filters the code list by 'Familia' 
        and 'Articulo' respectively
        """
        multi_index = pd.MultiIndex.from_tuples(filter_args, names=['Familia', 'Articulo'])
        filtered_df = df[df.set_index(['Familia', 'Articulo']).index.isin(multi_index)]

        filtered_df = self.common.delete_unnamed_cols(filtered_df)
    
        return filtered_df

    
    @execute_safely
    def filter_mov(self, df: pd.DataFrame, tipo: MovimientoEnum) -> pd.DataFrame:
        df = df.copy()
        df = self.common.delete_by_content(df, "Interno", INTERNOS_DEVOLUCION)
        df["Movimiento"] = df["Movimiento"].astype(str).str.strip()

        mask = False

        match tipo:
            case MovimientoEnum.SALIDAS:        mask = df["Movimiento"].isin(MOV_SALIDAS_LIST)
            case MovimientoEnum.ENTRADAS:       mask = df["Movimiento"].isin(MOV_ENTRADAS_LIST)
            case MovimientoEnum.DEVOLUCIONES:   mask = df["Movimiento"].isin(MOV_DEVOLUCIONES_LIST)
            case MovimientoEnum.TRANSFERENCIAS: mask = df["Movimiento"].isin(MOV_TRANSFERENCIAS_LIST)

        df = self.common.delete_unnamed_cols(df.loc[mask])

        return df
