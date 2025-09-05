import inspect

import pandas as pd

from typing import Union, Optional, List, Tuple, Literal

from src.config.constants import INTERNOS_DEVOLUCION, OUT_PATH, MOV_SALIDAS, MOV_ENTRADAS, MOV_DEVOLUCIONES, DEL_COLUMNS
from src.config.enums import SaveEnum
from src.services.utils.common_utils import CommonUtils
from src.services.utils.inventory_update import InventoryUpdate 
from src.services.utils.inventory_delete import InventoryDelete
from src.services.utils.exception_utils import execute_safely

class InventoryDataCleaner:
    def __init__(self, file: Union[str, pd.DataFrame], directory: Optional[str] = None, save: Literal["GUARDAR", "NO GUARDAR"] = "NO GUARDAR"):
        self.file = file
        self.directory = directory
        self.save = save
        self.utils = CommonUtils()
        self.delete = InventoryDelete()
        self.update = InventoryUpdate()
        self.df = self.utils.convert_to_df(self.file)
    
    def __str__(self):
        return f"New file name: {self.file} | Selected xlsx directoryectory: {self.directory}"
    

    def run_all(self)-> pd.DataFrame:
        """
        Arregla el listado de existencias de la siguiente forma:
        - Transforma todos los xls a xlsx.
        - Concatena todos los archivos en uno solo.
        - Elimina las columns innecesarias.
        - Filtra por salida.
        """
        df = self.utils.append_df(self.file, self.directory, self.save) # type: ignore
        df = self._transform(df)
        df = self.delete.unnamed_cols(df) # type: ignore

        if df is not None:
            return self.filter_mov(df, "salida")
        return pd.DataFrame()


    @execute_safely
    def _transform(self, df_list: pd.DataFrame) -> Optional[pd.DataFrame]:
        try:
            df_list.drop(columns=DEL_COLUMNS, inplace=True, axis=0)
        except KeyError:
            print("No se pueden eliminar las columnas, no existen.")
            pass


        df_updated = self.update.column_by_dict(df_list, "columns")
    
        df_updated["FechaCompleta"] = pd.to_datetime(df_updated["FechaCompleta"], format="%d/%m/%Y", errors="coerce", dayfirst=True)
        df_updated["Fecha"] = df_updated["FechaCompleta"].dt.strftime("%Y-%m")

        df_updated = self.update.rows_by_dict(df_updated, "depositos", "Cabecera")
        
        if self.save == SaveEnum.SAVE.value:
            df_updated.to_excel(f'{OUT_PATH}/{self.file}.xlsx', index=True)
        return df_updated


    @execute_safely
    def filter(self, column: str, filter_args: str, filter_type: str):
        nombre_funcion = inspect.currentframe().f_code.co_name # type: ignore

        match filter_type:
            case "contains" if self.df is not None:
                filtered_df = self.df.loc[self.df[column].str.contains(filter_args, na=False)] 
            case "startswith" if self.df is not None:
                filtered_df = self.df.loc[self.df[column].str.startswith(filter_args, na=False)]

        filtered_df = self.delete.unnamed_cols(filtered_df)

        if self.save == SaveEnum.SAVE.value:
            filtered_df.to_excel(f"{OUT_PATH}/{nombre_funcion}.xlsx")
        return filtered_df
    

    @execute_safely
    def filter_codigo(self, filter_args: float) -> pd.DataFrame:
        nombre_funcion = inspect.currentframe().f_code.co_name # type: ignore

        if self.df is not None:
            filtered_df = self.df.loc[self.df["Codigo"] == filter_args]

        filtered_df = self.delete.unnamed_cols(filtered_df)

        if self.save == SaveEnum.SAVE.value:
            filtered_df.to_excel(f"{OUT_PATH}/{nombre_funcion}.xlsx")
        return filtered_df
        
    
    @execute_safely
    def filter_lista_codigos(self, filter_args: Union[List, Tuple]) -> pd.DataFrame:
        """ Filters the code list by 'Familia' and 'Articulo' respectively"""
        nombre_funcion = inspect.currentframe().f_code.co_name # type: ignore

        if self.df is not None:
            filtered_df = pd.concat([self.df.loc[(self.df["Familia"] == fam) & 
                                                 (self.df["Articulo"] == art)] for fam, art in filter_args])
            
        filtered_df = self.delete.unnamed_cols(filtered_df)
    
        if self.save == SaveEnum.SAVE.value:
            filtered_df.to_excel(f"{OUT_PATH}/{nombre_funcion}.xlsx")
        return filtered_df

    
    @execute_safely
    def filter_mov(self, file: Union[pd.DataFrame, str], mov: Literal["salida", "entrada", "devolucion"]) -> pd.DataFrame:
        df_interno = self.delete.by_content(file, "Interno", INTERNOS_DEVOLUCION)
        
        match mov:
            case "salida":
                df = df_interno.loc[df_interno["Movimiento"].str.contains(MOV_SALIDAS, regex=True, na=False)]
            case "entrada":
                df = df_interno.loc[df_interno["Movimiento"].str.contains(MOV_ENTRADAS, regex=True, na=False)]
            case "devolucion" if self.df is not None:
                df = self.df.loc[self.df["Movimiento"].str.contains(MOV_DEVOLUCIONES, regex=True, na=False)]

        df = self.delete.unnamed_cols(df)

        if self.save == SaveEnum.SAVE.value:
            df.to_excel(f"{OUT_PATH}/{file}-mov.xlsx")
        return df

