import pandas as pd

from typing import Union, Optional, List

from plot_backend.general_utils import GeneralUtils
from plot_backend.utils_listado_existencias import UpdateListadoExistencias, DeleteListadoExistencias
from plot_backend.constants import INTERNOS_DEVOLUCION, MAIN_PATH

# TODO abstraer mas el programa y aplicar 

class ArreglarListadoExistencias:
    def __init__(self, filename: str, dir_files: Optional[str] = None):
        self.file = filename
        self.xlsx_dir = dir_files

        self._utils = GeneralUtils(self.file, self.xlsx_dir)


    def __str__(self):
        return f"New file name: {self.file} | Selected xlsx directory: {self.xlsx_dir}"
    

    def arreglar_listado(self) -> None:
        """
        Arregla el listado de existencias de la siguiente forma:
        - Transforma todos los xls a xlsx.
        - Concatena todos los archivos en uno solo.
        - Elimina las columnas innecesarias.
        - Filtra por salida.
        """
        try:
            df = self._utils.append_df(False)
            self.modify_df(df) # type: ignore
            self.filter("movimiento", "salidas")
            
        except pd.errors.InvalidIndexError as e:
            print(f"InvalidIndex -> {e}")
        except AttributeError as e:
            print(f"ERROR, atributo no encontrado -> {e}")
        except KeyError:
            print("ERROR: No existen las columnas, no se puede concatenar")


    def modify_df(self, df_list: pd.DataFrame) -> pd.DataFrame:
        """Applies the base modification to the 'Listado de existencias'"""

        try:
            df_list.drop(columns=["ficdep", "fictra", "artipo", "ficpro", "pronom", "ficrem", "ficfac", "corte", "signo", "transfe", "ficmov"], inplace=True, axis=0)
            
            _update_listado = UpdateListadoExistencias(df_list, self.xlsx_dir) #type: ignore
            df_list = _update_listado.update_column_by_dict("columnas")

            _update_listado = UpdateListadoExistencias(df_list, self.xlsx_dir) #type: ignore
            df_list = _update_listado.update_rows_by_dict("depositos", "Cabecera")
        except KeyError as r:
            print(f"Ya existen las columnas, no se cambiarán | ---> {r}")
            pass
        except OSError as e:
                print("No puede encontrar el archivo")
                print(f"OSError ---> {e}")
        
        df_list.to_excel(f'{MAIN_PATH}/excel/{self.file}.xlsx', index=True)
        return df_list


    def filter(self, column: str, filter: Union[str, float, List[str]], type: Optional[str] = None) -> pd.DataFrame:
        """
        Filters the file entered.\n
        - Columns: movimiento, repuesto, interno, codigo, lista_codigos\n
        - Types: None, contains, startswith
        """
        name: str = f"{self.file}-S"

        df = self._utils.check_filetype() # type: ignore
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
                            (df["Familia"] == fam) & #type: ignore
                            (df["Articulo"] == art)
                            ])
                    
                    filtered_df = pd.concat(filtered_df_list)
            case "movimiento":
                _delete_listado = DeleteListadoExistencias(self.file)
        
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
                        df: pd.DataFrame = self._utils.check_filetype() # type: ignore
                        name: str = f"{self.file}-D"

                        filtered_df: pd.DataFrame = df.loc[
                            df.Movimiento.str.contains("Devolucion")
                            ]
                    case _:
                        return pd.DataFrame()
            case _:
                return pd.DataFrame()

        if filtered_df.columns.str.contains("Unnamed").any():
            _delete_listado = DeleteListadoExistencias(filtered_df)
            filtered_df = _delete_listado.delete_unnamed_cols()

            if not isinstance(filter, list):
                filtered_df.to_excel(f"{MAIN_PATH}/excel/{name}.xlsx", index=True)
            else:
                filtered_df.to_excel(f"{MAIN_PATH}/excel/filtrado.xlsx")
        else:
            if not isinstance(filter, list):
                filtered_df.to_excel(f"{MAIN_PATH}/excel/{name}.xlsx")
            else:
                filtered_df.to_excel(f"{MAIN_PATH}/excel/filtrado.xlsx")
                
        return filtered_df
