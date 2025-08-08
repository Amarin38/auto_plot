import os 
import glob
import re

import pandas as pd
import numpy as np

from pathlib import Path
from typing import List, Union

from plot_backend.general_utils import GeneralUtils
from plot_backend.utils_listado_existencias import UtilsListadoExistencias


class ArreglarListadoExistencias:
    def __init__(self, filename: str, xlsx_dir: str):
        self.file = filename
        self._main_path = Path.cwd()
        self.xlsx_dir = xlsx_dir

        self._utils = GeneralUtils(self.file)
        self._utils_listado = UtilsListadoExistencias(self.file)
        self._xlsx_files = glob.glob(f"{self._main_path}/{self.xlsx_dir}/**/*.xlsx", recursive=True)

    def __str__(self):
        return f"New file name: {self.file} | Selected xlsx directory: {self.xlsx_dir}"


    def append_df(self) -> pd.DataFrame:
        """
        Appends all the xlsx files into one single file with 
        the name entered. 
        """
        if self._utils_listado.check_file_exists():
            print(f"Ya existe el archivo {self.file}")
            return pd.DataFrame()
        else:
            self._utils.xls_to_xlsx()
            df_list: List[str] = [] # type: ignore

            for file in self._xlsx_files:
                df_list.append(pd.read_excel(file, engine="calamine")) # type: ignore
            
            df_list: pd.DataFrame = pd.concat(df_list) # type: ignore
            df_list = self.modify_df(df_list)

            df_list.to_excel(f'{self._main_path}/excel/{self.file}.xlsx', index=True)
            return df_list 


    def modify_df(self, df_list: pd.DataFrame) -> pd.DataFrame:
        try:
            df_list.drop(columns=["ficdep", "fictra", "artipo", "ficpro", "pronom", "ficrem", "ficfac", "corte", "signo", "transfe", "ficmov"], inplace=True, axis=0)
            df_list = self._utils_listado.update_column_by_dict(df_list, "columnas")
            df_list = self._utils_listado.update_rows_by_dict(df_list, "depositos", "Cabecera")
        except KeyError as r:
            print(f"Ya existen las columnas, no se cambiarán | ---> {r}")
            pass
        except OSError as e:
                print("No puede encontrar el archivo")
                print(f"OSError ---> {e}")
        return df_list


    def basic_filter(self, filter: str) -> None:
        """
        Filters the main xlsx file into the desired replacement part movement type.\n
        Filter values: 'salidas', 'entradas', 'devoluciones'
        """
        
        internos_devolucion: np.ndarray = np.array(["C0488", "C0489", "C0500", "C0700", "C1400", 
                                                    "C4500", "C4900", "C6000", "C6700", "C9500",
                                                    "C9100", "C7000", "C5000", "C9000", "C3000",
                                                    "C4800", "C4700", "U4000", "C6600", "C6400",
                                                    "C0199", "C0599", "C0799", "C1499", "C4599", 
                                                    "C4999", "C6099", "C6799", "C9599", "C9199",
                                                    "C7099", "C5099", "C9099", "C3099", "C4899", 
                                                    "C4799", "C5599", "C6699", "C6199", "U1111"])
        
        match filter:
            case "salidas":
                df: pd.DataFrame = self._utils_listado.delete_rows("interno", internos_devolucion)
                name: str = f"{self.file}-S"

                filtrado_df: pd.DataFrame = df.loc[
                    (df.Movimiento.str.contains("Transf al Dep ")) | 
                    (df.Movimiento.str.contains("Salida"))
                    ]
            case "entradas":
                df: pd.DataFrame = self._utils_listado.delete_rows("interno", internos_devolucion)
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
            filtrado_df = self._utils_listado.delete_unnamed_cols(filtrado_df)
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