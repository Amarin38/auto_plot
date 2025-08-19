import pandas as pd

from typing import Union, Optional, List

from config.constants import INTERNOS_DEVOLUCION, MAIN_PATH
from src.services.utils.common_utils import CommonUtils
from src.services.data_cleaning.utils.inventory_update import InventoryUpdate 
from src.services.data_cleaning.utils.inventory_delete import InventoryDelete


class InventoryDataCleaner:
    def __init__(self, file: str, dir: Optional[str] = None):
        self.file = file
        self.dir = dir

        self._utils = CommonUtils(self.file, self.dir)


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
        try:
            df = self._utils.append_df(False)
            self.transform(df) # type: ignore
            self.filter("movimiento", "salidas")
            
        except pd.errors.InvalidIndexError as e:
            print(f"InvalidIndex -> {e}")
        except AttributeError as e:
            print(f"ERROR, atributo no encontrado -> {e}")
        except KeyError:
            print("ERROR: No existen las columns, no se puede concatenar")


    # TODO probar con replace
    def transform(self, df_list: pd.DataFrame) -> pd.DataFrame:
        """Applies the base modification to the 'Listado de existencias'"""

        try:
            df_list.drop(columns=["ficdep", "fictra", "artipo", "ficpro", "pronom", "ficrem", "ficfac", "corte", "signo", "transfe", "ficmov"], inplace=True, axis=0)
            
            _update_listado = InventoryUpdate(df_list, self.dir) #type: ignore
            df_list = _update_listado.update_column_by_dict("columns")

            _update_listado = InventoryUpdate(df_list, self.dir) #type: ignore
            df_list = _update_listado.update_rows_by_dict("depositos", "Cabecera")
        except KeyError as r:
            print(f"Ya existen las columns, no se cambiarán | ---> {r}")
            pass
        except OSError as e:
                print("No puede encontrar el file")
                print(f"OSError ---> {e}")
        
        df_list.to_excel(f'{MAIN_PATH}/out/{self.file}.xlsx', index=True)
        return df_list


    def filter(self, column: str, filter: Union[str, float, List[str]], type: Optional[str] = None) -> pd.DataFrame:
        """
        Filters the file entered.\n
        - Columns: movimiento, repuesto, interno, codigo, lista_codigos\n
        - Types: None, contains, startswith
        """
        name: str = f"{self.file}-S"

        df = self._utils.convert_to_df() # type: ignore
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
                    filtered_df = df.loc[df["Codigo"] == float(filter)]
            case "lista_codigos":
                if isinstance(filter, list):
                    filtered_df_list = []
                    
                    for fam, art in filter:
                        filtered_df_list.append(df.loc[
                            (df["Familia"] == fam) & 
                            (df["Articulo"] == art)
                            ])
                    
                    filtered_df = pd.concat(filtered_df_list)
            case "movimiento":
                _delete_listado = InventoryDelete(self.file)
        
                match filter:
                    case "salidas":
                        df: pd.DataFrame = _delete_listado.delete_rows("interno", INTERNOS_DEVOLUCION)

                        filtered_df: pd.DataFrame = df.loc[
                            (df.Movimiento.str.contains("Transf al Dep ")) | 
                            (df.Movimiento.str.contains("Salida"))
                            ]
                    case "entradas":
                        df: pd.DataFrame = _delete_listado.delete_rows("interno", INTERNOS_DEVOLUCION)
                        name: str = f"{self.file}-E"

                        filtered_df: pd.DataFrame = df.loc[
                            (df.Movimiento.str.contains("Tranf desde ")) |
                            (df.Movimiento.str.contains("Transf Recibida")) | 
                            (df.Movimiento.str.contains("Entrada "))
                            ]
                    case "devoluciones":
                        df: pd.DataFrame = self._utils.convert_to_df() # type: ignore
                        name: str = f"{self.file}-D"

                        filtered_df: pd.DataFrame = df.loc[
                            df.Movimiento.str.contains("Devolucion")
                            ]
                    case _:
                        return pd.DataFrame()
            case _:
                return pd.DataFrame()

        if filtered_df.columns.str.contains("Unnamed").any():
            _delete_listado = InventoryDelete(filtered_df)
            filtered_df = _delete_listado.delete_unnamed_cols()

            if not isinstance(filter, list):
                filtered_df.to_excel(f"{MAIN_PATH}/out/{name}.xlsx", index=True)
            else:
                filtered_df.to_excel(f"{MAIN_PATH}/out/filtrado.xlsx")
        else:
            if not isinstance(filter, list):
                filtered_df.to_excel(f"{MAIN_PATH}/out/{name}.xlsx")
            else:
                filtered_df.to_excel(f"{MAIN_PATH}/out/filtrado.xlsx")
                
        return filtered_df
