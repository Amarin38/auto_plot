import re
import glob
import os

import pandas as pd
import pyexcel as pe

from pathlib import Path
from typing import Optional, Union

from config import MAIN_PATH


class CommonUtils:
    @staticmethod
    def _check_file_exists(file: str) -> Optional[bool]:
        """
        Checks if the entered file name already exists.
        """
        try:
            return Path(f"{MAIN_PATH}/out/{file}.xlsx").exists()
        except UnboundLocalError:
            print("O la carpeta no existe o no se ingresó ninguna carpeta como parámetro")                         


    @staticmethod
    def _convert_to_df(file: Union[str, pd.DataFrame]) -> Optional[pd.DataFrame]:
        """
        Checks whereas the file entered is a string and converts it to dataframe \n
        and returns it or is already a dataframe and returns it.
        """
        try:
            if isinstance(file, str):
                return pd.read_excel(f"{MAIN_PATH}/out/{file}.xlsx", engine="calamine")
            else:
                return pd.DataFrame(file)
        except FileNotFoundError:
            pass
            # print(f"No existe el file para checkear o La carpeta esta vacía-> {e}")


    def _convert_xls_to_xlsx(self) -> None:
        """
        Converts all the .xls files in the current directory into a fully working .xlsx file\n
        deleting all the errors within the out .xls file.
        """
        _xls_files = glob.glob("**/*.xls", recursive=True)
        
        for file in _xls_files:
            file_mod_name = file.replace(".xls", "")

            try:
                df: pd.DataFrame = pd.read_excel(file, engine="xlrd")
                df["pronom"] = [self._delete_error_bytes(str(string), "\x00") if pd.notnull(string) else string for string in df["pronom"]]
                df.to_excel(f"{file_mod_name}.xlsx")
            except AssertionError:
                sheet = pe.get_sheet(file_name=file)
                sheet.save_as(file_mod_name)

            os.remove(file)


    def _append_df(self, file: str, dir: str, save: bool) -> Optional[pd.DataFrame]:
        """
        Appends all the xlsx files into one single file with 
        the name entered. 
        """

        if self._check_file_exists(file):
            return pd.DataFrame()
        else:
            self._convert_xls_to_xlsx()
            _xlsx_files = glob.glob(f"{MAIN_PATH}/{dir}/**/*.xlsx", recursive=True)

            try:
                df_list: pd.DataFrame = pd.concat([pd.read_excel(file, engine="calamine") for file in _xlsx_files])
            except ValueError as e:
                print(f"No encuentra los archivos XLSX -> {e}")
                
            if save:
                df_list.to_excel("appended_df.xlsx", index=False)
            else:
                return df_list
    

    @staticmethod
    def _delete_error_bytes(string: str, eliminar: str) -> str:
        return re.sub(fr"{eliminar}", "", string)