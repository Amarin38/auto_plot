import inspect

import pandas as pd

from typing import Union, List, Tuple, Literal

from src.config.constants import INTERNOS_DEVOLUCION, MOV_SALIDAS, MOV_ENTRADAS, MOV_DEVOLUCIONES, DEL_COLUMNS

from src.utils.exception_utils import execute_safely
from src.utils.common_utils import CommonUtils


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
            df = self.common.del_unnamed_cols(df)

            return self.filter_mov(df, "salida")
        return pd.DataFrame()


    @execute_safely
    def _transform(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            df = df.drop(columns=DEL_COLUMNS, axis=0)
        except KeyError:
            print("No se pueden eliminar las columnas, no existen.")
            pass

        df_updated = self.common.upd_column_by_dict(df, "columns")

        df_updated["FechaCompleta"] = pd.to_datetime(df_updated["FechaCompleta"], format="%d/%m/%Y", errors="coerce", dayfirst=True)
        df_updated["Fecha"] = df_updated["FechaCompleta"].dt.strftime("%Y-%m")

        df_updated = self.common.upd_rows_by_dict(df_updated, "depositos", "Cabecera")
        
        return df_updated


    @execute_safely
    def filter(self, df: pd.DataFrame, column: str, filter_args: str, filter_type: str):
        match filter_type:
            case "contains": filtered_df = df.loc[df[column].str.contains(filter_args, na=False)] 
            case "startswith": filtered_df = df.loc[df[column].str.startswith(filter_args, na=False)]

        filtered_df = self.common.del_unnamed_cols(filtered_df)

        return filtered_df
    

    @execute_safely
    def filter_codigo(self, df: pd.DataFrame, filter_args: float) -> pd.DataFrame:
        filtered_df = df.loc[df["Codigo"] == filter_args]
        filtered_df = self.common.del_unnamed_cols(filtered_df)

        return filtered_df
        
    
    @execute_safely
    def filter_lista_codigos(self, df: pd.DataFrame, filter_args: Union[List, Tuple]) -> pd.DataFrame:
        """ 
        Filters the code list by 'Familia' 
        and 'Articulo' respectively
        """
        filtered_df = pd.concat([df.loc[(df["Familia"] == fam) & 
                                        (df["Articulo"] == art)] for fam, art in filter_args])
            
        filtered_df = self.common.del_unnamed_cols(filtered_df)
    
        return filtered_df

    
    @execute_safely
    def filter_mov(self, df: pd.DataFrame, mov: Literal["salida", "entrada", "devolucion"]) -> pd.DataFrame:
        df = self.common.del_by_content(df, "Interno", INTERNOS_DEVOLUCION)
        
        match mov:
            case "salida": df_final = df.loc[df["Movimiento"].str.contains(MOV_SALIDAS, regex=True, na=False)]
            case "entrada": df_final = df.loc[df["Movimiento"].str.contains(MOV_ENTRADAS, regex=True, na=False)]
            case "devolucion": df_final = df.loc[df["Movimiento"].str.contains(MOV_DEVOLUCIONES, regex=True, na=False)]

        df_final = self.common.del_unnamed_cols(df_final)

        return df_final

