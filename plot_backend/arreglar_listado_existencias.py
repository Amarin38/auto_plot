import os 
import glob
import re

import pandas as pd

from pathlib import Path
from typing import List, Union

from utils_listado_existencias import UtilsListadoExistencias

#TODO aplicar multithreading

class ArreglarListadoExistencias:
    def __init__(self, filename: str, xlsx_dir: str):
        self.file = filename
        self.xlsx_dir = xlsx_dir
        self._utils = UtilsListadoExistencias(self.file)

        self._main_path = Path.cwd()
        self._xls_files = glob.glob("**/*.xls", recursive=True)
        self._xlsx_files = glob.glob(f"{self._main_path}/{self.xlsx_dir}/**/*.xlsx", recursive=True)

    def __str__(self):
        return f"New file name: {self.file} | Selected xlsx directory: {self.xlsx_dir}"


    def check_file_exists(self) -> bool:
        """
        Checks if the entered file name already exists.
        """
        try:
            if os.path.exists(f"{self._main_path}/excel/{self.file}.xlsx"):
                return True
        except FileNotFoundError:
            return False
        else:
            return False


    def xls_to_xlsx(self) -> None:
        """
        Converts all the .xls files in the current directory into a fully working .xlsx file\n
        deleting all the errors within the excel .xls file.
        """
        
        for file in self._xls_files:
            df: pd.DataFrame = pd.read_excel(file, engine="xlrd")
            # Leer el archivo y eliminar caracteres nulos
            
            df["pronom"] = [self.delete_error_bytes(str(string), "\x00") if pd.notnull(string) else string for string in df["pronom"]]

            file_mod = file.replace(".xls", "")
            df.to_excel(f"{file_mod}.xlsx")
            os.remove(file)


    def append_df(self) -> pd.DataFrame:
        """
        Appends all the xlsx files into one single file with 
        the name entered. 
        """
        if self.check_file_exists():
            return pd.DataFrame()
        else:
            self.xls_to_xlsx()
            df_list: List[str] = [] # type: ignore

            for file in self._xlsx_files:
                df_list.append(pd.read_excel(file, engine="calamine")) # type: ignore
            
            df_list: pd.DataFrame = pd.concat(df_list) # type: ignore
            df_list = self.modify_df(df_list)

            # if df_list.columns.str.contains("Unnamed").any():
            #     df_list = self._utils.delete_unnamed_cols(df_list)

            df_list.to_excel(f'{self._main_path}/excel/{self.file}.xlsx', index=False)
            return df_list 


    def modify_df(self, df_list: pd.DataFrame) -> pd.DataFrame:
        try:
            df_list.drop(columns=["ficdep", "fictra", "artipo", "ficpro", "pronom", "ficrem", "ficfac", "corte", "signo", "transfe", "ficmov"], inplace=True, axis=0)
            df_list = self._utils.update_column_by_dict(df_list, "columnas")
            df_list = self._utils.update_rows_by_dict(df_list, "depositos", "Cabecera")
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
        
        internos_devolucion: List[str] = ["C0488", "C0489", "C0500", "C0700", "C1400", 
                                          "C4500", "C4900", "C6000", "C6700", "C9500",
                                          "C9100", "C7000", "C5000", "C9000", "C3000",
                                          "C4800", "C4700", "U4000", "C6600", "C6400",
                                          "C0199", "C0599", "C0799", "C1499", "U2000",
                                          "C4599", "C4999", "C6099", "C6799", "C9599",
                                          "C9199", "C7099", "C5099", "C9099", "C3099",
                                          "C4899", "C4799", "C5599", "C6699", "C6199"]

        match filter:
            case "salidas":
                df: pd.DataFrame = self._utils.delete_rows("interno", internos_devolucion)

                filtrado_df: pd.DataFrame = df.loc[
                    (df.Movimiento.str.contains("Transf al Dep ")) | 
                    (df.Movimiento.str.contains("Salida"))
                    ]

                if filtrado_df.columns.str.contains("Unnamed").any():
                    filtrado_df = self._utils.delete_unnamed_cols(filtrado_df)
                filtrado_df.to_excel(f"{self._main_path}/excel/{self.file}-S.xlsx", index=False)

            case "entradas":
                df: pd.DataFrame = self._utils.delete_rows("interno", internos_devolucion)

                filtrado_df: pd.DataFrame = df.loc[
                    df.Movimiento.str.contains("Tranf desde ") |
                    df.Movimiento.str.contains("Transf Recibida") | 
                    df.Movimiento.str.contains("Entrada ") 
                    ]

                if filtrado_df.columns.str.contains("Unnamed").any():
                    filtrado_df = self._utils.delete_unnamed_cols(filtrado_df)
                filtrado_df.to_excel(f"{self._main_path}/excel/{self.file}-E.xlsx", index=False)

            case "devoluciones":
                df: pd.DataFrame = self.check_filetype(self.file)

                filtrado_df: pd.DataFrame = df.loc[
                    df.Movimiento.str.contains("Devolucion")
                    ]
            
                if filtrado_df.columns.str.contains("Unnamed").any():
                    filtrado_df = self._utils.delete_unnamed_cols(filtrado_df)
                filtrado_df.to_excel(f"{self._main_path}/excel/{self.file}-D.xlsx", index=False)     

            case _:
                return None


    def filter_by(self, column: str, type: str, filter: str) -> pd.DataFrame:
        """
        Filters the file entered by string entered in the filters var.\n
        Indicating the column is needed.\n 
        Columns: repuesto, interno\n
        Types: contains, startswith
        """
        df: pd.DataFrame = self.check_filetype(self.file)

        match column:
            case "repuesto":
                if type == "contains":
                    filtered_df = df.loc[df.Repuesto.str.contains(filter, na=False)]
                elif type == "startswith":
                    filtered_df = df.loc[df.Repuesto.str.startswith(filter, na=False)]
            case "interno":
                if type == "contains":
                    filtered_df = df.loc[df.Interno.str.contains(filter, na=False)]
                elif type == "startswith":
                    filtered_df = df.loc[df.Interno.str.startswith(filter, na=False)]
            case _:
                return pd.DataFrame()

        filtered_df.to_excel(f"{self._main_path}/excel/{filter}.xlsx")
        return filtered_df


    # --- UTILS --- #
    def delete_error_bytes(self, string: str, eliminar: str) -> str:
        return re.sub(fr"{eliminar}", "", string)


    def check_filetype(self, file: Union[str, pd.DataFrame]):
        if isinstance(file, str):
            df: pd.DataFrame = pd.read_excel(f"{self._main_path}/excel/{file}.xlsx", engine="calamine", index_col=0)
        else:
            df: pd.DataFrame = pd.DataFrame(file)
        
        return df


if __name__ == '__main__':    
    arreglar = ArreglarListadoExistencias("todas-herramientas", "todas herramientas")
    # arreglar.append_df()
    # arreglar.basic_filter("salidas")
    arreglar.filter_by("repuesto", "contains", "")
    # arreglar.filter_by("", "contains", "LUNETA")
    # arreglar.filter_by("", "contains", "PARABRISA")


    # utils = UtilsListadoExistencias("inyectores-S")
    # utils.rename_rows_by_dict("inyectores-S", "motores", "Repuesto")
    # utils.delete_rows("repuesto", "CAÑO")
    # utils.drop_unnamed_cols("inyectores-S")
    # arreglar.append_df()
    # arreglar.delete_remain_rows("repuesto", "CAÑO")