import pandas as pd

from pathlib import Path
from typing import Union

from plot_backend.general_utils import GeneralUtils
from plot_backend.utils_listado_existencias import UpdateListadoExistencias, DeleteListadoExistencias
from plot_backend.constants import INTERNOS_DEVOLUCION

# TODO abstraer mas el programa y aplicar 

class ArreglarListadoExistencias:
    def __init__(self, filename: str, xlsx_dir: str):
        self.file = filename
        self._main_path = Path.cwd()
        self.xlsx_dir = xlsx_dir

        self._utils = GeneralUtils(self.file, self.xlsx_dir)

    def __str__(self):
        return f"New file name: {self.file} | Selected xlsx directory: {self.xlsx_dir}"
    

    def modify_df(self, df_list: pd.DataFrame) -> pd.DataFrame:
        _update_listado = UpdateListadoExistencias(df_list)

        try:
            df_list.drop(columns=["ficdep", "fictra", "artipo", "ficpro", "pronom", "ficrem", "ficfac", "corte", "signo", "transfe", "ficmov"], inplace=True, axis=0)
            df_list = _update_listado.update_column_by_dict("columnas")
            df_list = _update_listado.update_rows_by_dict("depositos", "Cabecera")
        except KeyError as r:
            print(f"Ya existen las columnas, no se cambiarán | ---> {r}")
            pass
        except OSError as e:
                print("No puede encontrar el archivo")
                print(f"OSError ---> {e}")
        
        df_list.to_excel(f'{self._main_path}/excel/{self.file}.xlsx', index=True)
        return df_list


    def basic_filter(self, filter: str) -> None:
        """
        Filters the main xlsx file into the desired replacement part movement type.\n
        Filter values: 'salidas', 'entradas', 'devoluciones'
        """
        _delete_listado = DeleteListadoExistencias(self.file)
        
        match filter:
            case "salidas":
                df: pd.DataFrame = _delete_listado.delete_rows("interno", INTERNOS_DEVOLUCION)
                name: str = f"{self.file}-S"

                filtrado_df: pd.DataFrame = df.loc[
                    (df.Movimiento.str.contains("Transf al Dep ")) | 
                    (df.Movimiento.str.contains("Salida"))
                    ]
            case "entradas":
                df: pd.DataFrame = _delete_listado.delete_rows("interno", INTERNOS_DEVOLUCION)
                name: str = f"{self.file}-E"

                filtrado_df: pd.DataFrame = df.loc[
                    (df.Movimiento.str.contains("Tranf desde ")) |
                    (df.Movimiento.str.contains("Transf Recibida")) | 
                    (df.Movimiento.str.contains("Entrada "))
                    ]
            case "devoluciones":
                df: pd.DataFrame = self._utils.check_filetype()
                name: str = f"{self.file}-D"

                filtrado_df: pd.DataFrame = df.loc[
                    df.Movimiento.str.contains("Devolucion")
                    ]
            case _:
                return None

        if filtrado_df.columns.str.contains("Unnamed").any():
            _delete_listado = DeleteListadoExistencias(filtrado_df)
            
            filtrado_df = _delete_listado.delete_unnamed_cols()
            filtrado_df.to_excel(f"{self._main_path}/excel/{name}.xlsx", index=True)


    def filter_by(self, column: str, type: str, filter: Union[str, float]) -> pd.DataFrame:
        """
        Filters the file entered by string entered in the filters var.\n
        Indicating the column is needed.\n 
        Columns: repuesto, interno, codigo\n
        Types: contains, startswith
        """

        df = self._utils.check_filetype()
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
            case _:
                return pd.DataFrame()

        filtered_df.to_excel(f"{self._main_path}/excel/{filter}.xlsx")
        return filtered_df


class ModificarExcel:
    pass

class FiltrarExcel:
    pass