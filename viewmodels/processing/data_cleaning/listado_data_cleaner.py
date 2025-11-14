from typing import Union, List, Tuple

import pandas as pd

from config.constants import INTERNOS_DEVOLUCION, MOV_SALIDAS, MOV_ENTRADAS, MOV_DEVOLUCIONES, DEL_COLUMNS, \
    PAGE_STRFTIME_DMY, DELTA_STRFTIME_YM
from config.enums import MovimientoEnum
from utils.common_utils import CommonUtils
from utils.exception_utils import execute_safely


class InventoryDataCleaner:
    def __init__(self):
        self.common = CommonUtils()


    def run_all(self, df_directory: list)-> pd.DataFrame:
        """
        Arregla el listado de existencias de la siguiente forma:
        - Transforma todos los xls a xlsx.
        - Concatena todos los archivos en uno solo.
        - Elimina las columns innecesarias.
        - Filtra por salida.
        """
        df: pd.DataFrame = self.common.concat_dataframes(df_directory)
        
        if not df.empty:
            df = self._transform(df)
            df = self.common.delete_unnamed_cols(df)

            return self.filter_mov(df, MovimientoEnum.SALIDAS)
        return pd.DataFrame()


    @execute_safely
    def _transform(self, df: pd.DataFrame) -> pd.DataFrame:
        # transformo las columnas para poder eliminarlas
        df.columns = df.columns.str.strip("'").str.strip()
        df.columns = [
            (col.decode('utf8', 'ignore')
            if isinstance(col, bytes) else col)
            for col in df.columns
        ]

        df_updated = self.common.update_columns(df, "columns")
        df_updated = df_updated.drop(columns=DEL_COLUMNS, axis=1, errors="ignore")

        df_updated["FechaCompleta"] = pd.to_datetime(df_updated["FechaCompleta"], format=PAGE_STRFTIME_DMY, errors="coerce", dayfirst=True)
        df_updated["Fecha"] = df_updated["FechaCompleta"].dt.strftime(DELTA_STRFTIME_YM)

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
        filtered_df = pd.concat([df.loc[(df["Familia"] == fam) & 
                                        (df["Articulo"] == art)] for fam, art in filter_args])
            
        filtered_df = self.common.delete_unnamed_cols(filtered_df)
    
        return filtered_df

    
    @execute_safely
    def filter_mov(self, df: pd.DataFrame, mov: MovimientoEnum) -> pd.DataFrame:
        df = self.common.delete_by_content(df, "Interno", INTERNOS_DEVOLUCION)

        match mov:
            case MovimientoEnum.SALIDAS: df = df.loc[df["Movimiento"].str.contains(MOV_SALIDAS, regex=True, na=False)]
            case MovimientoEnum.ENTRADAS: df = df.loc[df["Movimiento"].str.contains(MOV_ENTRADAS, regex=True, na=False)]
            case MovimientoEnum.DEVOLUCIONES: df = df.loc[df["Movimiento"].str.contains(MOV_DEVOLUCIONES, regex=True, na=False)]

        df = self.common.delete_unnamed_cols(df)

        return df

