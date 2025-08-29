import pandas as pd

from typing import Union, Optional, List

from config.constants import INTERNOS_DEVOLUCION, OUT_PATH
from ..utils.common_utils import CommonUtils
from ..utils.inventory_update import InventoryUpdate 
from ..utils.inventory_delete import InventoryDelete
from ..utils.exception_utils import execute_safely

class InventoryDataCleaner:
    def __init__(self, file: str, dir: Optional[str] = None):
        self.file = file
        self.dir = dir

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
        df = CommonUtils()._append_df(self.file, self.dir, save=True) # type: ignore
        print(df)
        self.transform(df) # type: ignore
        self.filter("movimiento", "salidas")



    # TODO: probar con replace
    @execute_safely
    def transform(self, df_list: pd.DataFrame) -> pd.DataFrame:
        """Applies the base modification to the 'Listado de existencias'"""

        try:
            df_list.drop(columns=["ficdep", "fictra", "artipo", "ficpro", "pronom", "ficrem", 
                                  "ficfac", "corte", "signo", "transfe", "ficmov"], inplace=True, axis=0)
        except KeyError or AttributeError:
            pass

        inv_upd = InventoryUpdate(df_list)
        df_updated = inv_upd._update_column_by_dict("columns")
        inv_upd = InventoryUpdate(df_updated)
        df_updated = inv_upd._update_rows_by_dict("depositos", "Cabecera")

        
        df_updated.to_excel(f'{OUT_PATH}/{self.file}.xlsx', index=True) # type:ignore
        return df_updated # type: ignore


    @execute_safely
    def filter(self, column: str, filter: Union[str, float, List[str]], type: Optional[str] = None) -> pd.DataFrame:
        """
        Filters the file entered.\n
        - Columns: movimiento, repuesto, interno, codigo, lista_codigos\n
        - Types: None, contains, startswith
        """
        df: pd.DataFrame = CommonUtils()._convert_to_df(self.file) # type: ignore

        match column:
            case "repuesto":
                if type == "contains" and isinstance(filter, str):
                    filtered_df = df.loc[df.Repuesto.str.contains(filter, na=False)]
                elif type == "startswith" and isinstance(filter, str):
                    filtered_df = df.loc[df.Repuesto.str.startswith(filter, na=False)]
            case "interno":
                if type == "contains" and isinstance(filter, str):
                    filtered_df = df.loc[df.Interno.str.contains(filter, na=False)]
                elif type == "startswith" and isinstance(filter, str):
                    filtered_df = df.loc[df.Interno.str.startswith(filter, na=False)]
            case "codigo":
                if isinstance(filter, float):
                    filtered_df = df.loc[df["Codigo"] == filter]
            case "lista_codigos":
                if isinstance(filter, list):
                    # filtered_df_list = []
                    
                    filtered_df = pd.concat([df.loc[(df["Familia"] == fam) & 
                                                    (df["Articulo"] == art)] for fam, art in filter])
                    # for fam, art in filter:
                    #     filtered_df_list.append(df.loc[
                    #         (df["Familia"] == fam) & 
                    #         (df["Articulo"] == art)
                    #         ])
                    # filtered_df = pd.concat(filtered_df_list)
            case "movimiento":
                delete_listado = InventoryDelete(self.file)
                df_del: pd.DataFrame = delete_listado._delete_rows("interno", INTERNOS_DEVOLUCION) # type: ignore

                match filter:
                    case "salidas":
                        name: str = f"{self.file}-S"

                        filtered_df: pd.DataFrame = df_del.loc[
                            (df_del.Movimiento.str.contains("Transf al Dep ")) | 
                            (df_del.Movimiento.str.contains("Salida"))
                            ]
                    case "entradas":
                        name: str = f"{self.file}-E"

                        filtered_df: pd.DataFrame = df_del.loc[
                            (df_del.Movimiento.str.contains("Tranf desde ")) |
                            (df_del.Movimiento.str.contains("Transf Recibida")) | 
                            (df_del.Movimiento.str.contains("Entrada "))
                            ]
                    case "devoluciones":
                        name: str = f"{self.file}-D"

                        filtered_df: pd.DataFrame = df.loc[df.Movimiento.str.contains("Devolucion")]
                    case _:
                        return pd.DataFrame()
            case _:
                return pd.DataFrame()

        if filtered_df.columns.str.contains("Unnamed").any():
            delete = InventoryDelete(filtered_df)
            filtered_df = delete._delete_unnamed_cols() # type: ignore

        if not isinstance(filter, list):
            filtered_df.to_excel(f"{OUT_PATH}/{name}.xlsx", index=True)
        else:
            filtered_df.to_excel(f"{OUT_PATH}/filtrado.xlsx")
        
        return filtered_df
