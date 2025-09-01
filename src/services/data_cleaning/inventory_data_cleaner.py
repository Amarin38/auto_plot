import inspect

import pandas as pd

from typing import Union, Optional, List, Tuple

from config.constants import INTERNOS_DEVOLUCION, OUT_PATH, MOV_SALIDAS, MOV_ENTRADAS, MOV_DEVOLUCIONES, DEL_COLUMNS
from ..utils.common_utils import CommonUtils
from ..utils.inventory_update import InventoryUpdate 
from ..utils.inventory_delete import InventoryDelete
from ..utils.exception_utils import execute_safely

class InventoryDataCleaner:
    def __init__(self, file: str, dir: Optional[str] = None):
        self.file = file
        self.dir = dir

        self.utils = CommonUtils()

        self.nombre_funcion = inspect.currentframe().f_code.co_name # type: ignore


    def __str__(self):
        return f"New file name: {self.file} | Selected xlsx directory: {self.dir}"
    

    def run_all(self) -> None:
        """
        Arregla el listado de existencias de la siguiente forma:
        - Transforma todos los xls a xlsx.
        - Concatena todos los archivos en uno solo.
        - Elimina las columns innecesarias.
        - Filtra por salida.
        """
        df = self.utils.append_df(self.file, self.dir, save="GUARDAR") # type: ignore
        self.transform(df) # type: ignore
        self.filter_mov_salidas()


    @execute_safely
    def transform(self, df_list: pd.DataFrame) -> pd.DataFrame:
        """Applies the base modification to the 'Listado de existencias'"""

        df_list.drop(columns=DEL_COLUMNS, inplace=True, axis=0)

        inv_upd = InventoryUpdate(df_list)
        df_updated = inv_upd._update_column_by_dict("columns")

        df_updated["FechaCompleta"] = pd.to_datetime(df_updated["FechaCompleta"], format="%d/%m/%Y", errors="coerce", dayfirst=True)
        df_updated["Fecha"] = df_updated["FechaCompleta"].dt.strftime("%Y-%m")

        inv_upd = InventoryUpdate(df_updated) # actualizo el objeto
        df_updated = inv_upd._update_rows_by_dict("depositos", "Cabecera")

        print(df_updated)
        
        df_updated.to_excel(f'{OUT_PATH}/{self.file}.xlsx', index=True) # type:ignore
        return df_updated # type: ignore


    @execute_safely
    def filter_repuesto(self, filter_args: str, filter_type: str) -> pd.DataFrame:
        df: pd.DataFrame = self.utils._convert_to_df(self.file) # type: ignore

        if filter_type == "contains":
            filtered_df = df.loc[df.Repuesto.str.contains(filter_args, na=False)]
        elif filter_type == "startswith":
            filtered_df = df.loc[df.Repuesto.str.startswith(filter_args, na=False)]
        
        if filtered_df.columns.str.contains("Unnamed").any():
            delete = InventoryDelete(filtered_df)
            filtered_df = delete._delete_unnamed_cols() # type: ignore

        filtered_df.to_excel(f"{OUT_PATH}/{self.nombre_funcion}.xlsx")
        return filtered_df


    @execute_safely
    def filter_interno(self, filter_args: str, filter_type: str) -> pd.DataFrame:
        df: pd.DataFrame = self.utils._convert_to_df(self.file) # type: ignore

        if filter_type == "contains":
            filtered_df = df.loc[df.Interno.str.contains(filter_args, na=False)]
        elif filter_type == "startswith":
            filtered_df = df.loc[df.Interno.str.startswith(filter_args, na=False)]

        if filtered_df.columns.str.contains("Unnamed").any():
            delete = InventoryDelete(filtered_df)
            filtered_df = delete._delete_unnamed_cols() # type: ignore

        filtered_df.to_excel(f"{OUT_PATH}/{self.nombre_funcion}.xlsx")
        return filtered_df


    @execute_safely
    def filter_codigo(self, filter_args: float) -> pd.DataFrame:
        df: pd.DataFrame = self.utils._convert_to_df(self.file) # type: ignore

        filtered_df = df.loc[df["Codigo"] == filter_args]

        if filtered_df.columns.str.contains("Unnamed").any():
            delete = InventoryDelete(filtered_df)
            filtered_df = delete._delete_unnamed_cols() # type: ignore

        filtered_df.to_excel(f"{OUT_PATH}/{self.nombre_funcion}.xlsx")
        return filtered_df
        
    
    @execute_safely
    def filter_lista_codigos(self, filter_args: Union[List, Tuple]) -> pd.DataFrame:
        df: pd.DataFrame = self.utils._convert_to_df(self.file) # type: ignore

        filtered_df = pd.concat([df.loc[(df["Familia"] == fam) & 
                                        (df["Articulo"] == art)] 
                                        for fam, art in filter_args])
        
        if filtered_df.columns.str.contains("Unnamed").any():
            delete = InventoryDelete(filtered_df)
            filtered_df = delete._delete_unnamed_cols() # type: ignore

        filtered_df.to_excel(f"{OUT_PATH}/{self.nombre_funcion}.xlsx")
        return filtered_df


    @execute_safely
    def filter_mov_salidas(self) -> pd.DataFrame:
        df_del: pd.DataFrame = InventoryDelete(self.file)._delete_rows("interno", INTERNOS_DEVOLUCION)

        filtered_df: pd.DataFrame = df_del.loc[df_del.Movimiento.str.contains(MOV_SALIDAS, regex=True)]

        if filtered_df.columns.str.contains("Unnamed").any():
            delete = InventoryDelete(filtered_df)
            filtered_df = delete._delete_unnamed_cols() # type: ignore

        filtered_df.to_excel(f"{OUT_PATH}/{self.file}-S.xlsx")
        return filtered_df


    @execute_safely
    def filter_mov_entradas(self) -> pd.DataFrame:
        df_del: pd.DataFrame = InventoryDelete(self.file)._delete_rows("interno", INTERNOS_DEVOLUCION)

        filtered_df: pd.DataFrame = df_del.loc[df_del.Movimiento.str.contains(MOV_ENTRADAS, regex=True)]

        if filtered_df.columns.str.contains("Unnamed").any():
            delete = InventoryDelete(filtered_df)
            filtered_df = delete._delete_unnamed_cols() # type: ignore

        filtered_df.to_excel(f"{OUT_PATH}/{self.file}-E.xlsx")
        return filtered_df


    @execute_safely
    def filter_mov_devoluciones(self) -> pd.DataFrame:
        df: pd.DataFrame = self.utils._convert_to_df(self.file) # type: ignore

        filtered_df: pd.DataFrame = df.loc[df.Movimiento.str.contains(MOV_DEVOLUCIONES, regex=True)]
        
        if filtered_df.columns.str.contains("Unnamed").any():
            delete = InventoryDelete(filtered_df)
            filtered_df = delete._delete_unnamed_cols() # type: ignore

        filtered_df.to_excel(f"{OUT_PATH}/{self.file}-D.xlsx")
        return filtered_df

