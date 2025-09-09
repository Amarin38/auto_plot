import inspect

import pandas as pd

from typing import Union, List, Tuple, Literal

from src.config.constants import INTERNOS_DEVOLUCION, OUT_PATH, MOV_SALIDAS, MOV_ENTRADAS, MOV_DEVOLUCIONES, DEL_COLUMNS
from src.config.enums import SaveEnum
from src.services.utils.common_utils import CommonUtils
from src.services.utils.inventory_update import InventoryUpdate 
from src.services.utils.inventory_delete import InventoryDelete
from src.services.utils.exception_utils import execute_safely

class InventoryDataCleaner:
    def __init__(self, save: Literal["SAVE", "NOT SAVE"] = "NOT SAVE"):
        self.save = save
        self.utils = CommonUtils()
        self.delete = InventoryDelete()
        self.update = InventoryUpdate()


    def run_all(self, directory: str)-> pd.DataFrame:
        """
        Arregla el listado de existencias de la siguiente forma:
        - Transforma todos los xls a xlsx.
        - Concatena todos los archivos en uno solo.
        - Elimina las columns innecesarias.
        - Filtra por salida.
        """
        df: pd.DataFrame = self.utils.append_df(directory)

        if not df.empty:
            df = self._transform(df)
            df = self.delete.unnamed_cols(df)

            return self.filter_mov(df, "salida")
        return pd.DataFrame()


    @execute_safely
    def _transform(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            df = df.drop(columns=DEL_COLUMNS, axis=0)
        except KeyError:
            print("No se pueden eliminar las columnas, no existen.")
            pass

        df_updated = self.update.column_by_dict(df, "columns")

        df_updated["FechaCompleta"] = pd.to_datetime(df_updated["FechaCompleta"], format="%d/%m/%Y", errors="coerce", dayfirst=True)
        df_updated["Fecha"] = df_updated["FechaCompleta"].dt.strftime("%Y-%m")

        df_updated = self.update.rows_by_dict(df_updated, "depositos", "Cabecera")
        
        if self.save == SaveEnum.SAVE.value:
            df_updated.to_excel(f'{OUT_PATH}/transformed.xlsx', index=True)
        return df_updated


    @execute_safely
    def filter(self, df: pd.DataFrame, column: str, filter_args: str, filter_type: str):
        nombre_funcion = inspect.currentframe().f_code.co_name # type: ignore

        match filter_type:
            case "contains":
                filtered_df = df.loc[df[column].str.contains(filter_args, na=False)] 
            case "startswith":
                filtered_df = df.loc[df[column].str.startswith(filter_args, na=False)]

        filtered_df = self.delete.unnamed_cols(filtered_df)

        if self.save == SaveEnum.SAVE.value:
            filtered_df.to_excel(f"{OUT_PATH}/{nombre_funcion}.xlsx")
        return filtered_df
    

    @execute_safely
    def filter_codigo(self, df: pd.DataFrame, filter_args: float) -> pd.DataFrame:
        nombre_funcion = inspect.currentframe().f_code.co_name # type: ignore

        filtered_df = df.loc[df["Codigo"] == filter_args]
        filtered_df = self.delete.unnamed_cols(filtered_df)

        if self.save == SaveEnum.SAVE.value:
            filtered_df.to_excel(f"{OUT_PATH}/{nombre_funcion}.xlsx")
        return filtered_df
        
    
    @execute_safely
    def filter_lista_codigos(self, df: pd.DataFrame, filter_args: Union[List, Tuple]) -> pd.DataFrame:
        """ Filters the code list by 'Familia' and 'Articulo' respectively"""
        nombre_funcion = inspect.currentframe().f_code.co_name # type: ignore

        filtered_df = pd.concat([df.loc[(df["Familia"] == fam) & 
                                        (df["Articulo"] == art)] for fam, art in filter_args])
            
        filtered_df = self.delete.unnamed_cols(filtered_df)
    
        if self.save == SaveEnum.SAVE.value:
            filtered_df.to_excel(f"{OUT_PATH}/{nombre_funcion}.xlsx")
        return filtered_df

    
    @execute_safely
    def filter_mov(self, df: pd.DataFrame, mov: Literal["salida", "entrada", "devolucion"]) -> pd.DataFrame:
        df_interno = self.delete.by_content(df, "Interno", INTERNOS_DEVOLUCION)
        
        match mov:
            case "salida":
                df_final = df_interno.loc[df_interno["Movimiento"].str.contains(MOV_SALIDAS, regex=True, na=False)]
            case "entrada":
                df_final = df_interno.loc[df_interno["Movimiento"].str.contains(MOV_ENTRADAS, regex=True, na=False)]
            case "devolucion":
                df_final = df.loc[df["Movimiento"].str.contains(MOV_DEVOLUCIONES, regex=True, na=False)]

        df_final = self.delete.unnamed_cols(df_final)

        return df_final

