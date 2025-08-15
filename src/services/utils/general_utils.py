import re
import glob
import os

import pandas as pd
import pyexcel as pe

from pathlib import Path
from typing import Union, Optional, List

from src.config.constants import MAIN_PATH

class GeneralUtils:
    def __init__(self, file: Union[str, pd.DataFrame], xlsx_dir: Optional[str] = None) -> None:
        self.file = file
        self._xlsx_dir = xlsx_dir


    def check_file_exists(self) -> Optional[bool]:
        """
        Checks if the entered file name already exists.
        """
        try:
            return Path(f"{MAIN_PATH}/out/{self.file}.xlsx").exists()
        except UnboundLocalError:
            print("O la carpeta no existe o no se ingresó ninguna carpeta como parámetro")                         


    def check_filetype(self) -> Optional[pd.DataFrame]:
        """
        Checks whereas the file entered is a string and converts it to dataframe \n
        and returns it or is already a dataframe and returns it.
        """
        try:
            if isinstance(self.file, str):
                return pd.read_excel(f"{MAIN_PATH}/out/{self.file}.xlsx", engine="calamine")
            else:
                return pd.DataFrame(self.file)
        except FileNotFoundError:
            pass
            # print(f"No existe el archivo para checkear o La carpeta esta vacía-> {e}")

    
    def xls_to_xlsx(self) -> None:
        """
        Converts all the .xls files in the current directory into a fully working .xlsx file\n
        deleting all the errors within the out .xls file.
        """
        _xls_files = glob.glob("**/*.xls", recursive=True)
        
        for file in _xls_files:
            file_mod = file.replace(".xls", "")

            try:
                df: pd.DataFrame = pd.read_excel(file, engine="xlrd")
                df["pronom"] = [self._delete_error_bytes(str(string), "\x00") if pd.notnull(string) else string for string in df["pronom"]]
                df.to_excel(f"{file_mod}.xlsx")
            except AssertionError:
                sheet = pe.get_sheet(file_name=file)
                sheet.save_as(file_mod)

            os.remove(file)


    def append_df(self, guardar: bool) -> Optional[pd.DataFrame]:
        """
        Appends all the xlsx files into one single file with 
        the name entered. 
        """

        if self.check_file_exists():
            return pd.DataFrame()
        else:
            self.xls_to_xlsx()
            df_list: List[str] = [] # type: ignore

            _xlsx_files = glob.glob(f"{MAIN_PATH}/{self._xlsx_dir}/**/*.xlsx", recursive=True)

            for file in _xlsx_files:
                df_list.append(pd.read_excel(file, engine="calamine")) # type: ignore
            
            df_list: pd.DataFrame = pd.concat(df_list) # type: ignore

            if guardar:
                df_list.to_excel("appended_df.xlsx", index=False)
            else:
                return df_list
    

    @staticmethod
    def _delete_error_bytes(string: str, eliminar: str) -> str:
        return re.sub(fr"{eliminar}", "", string)
    
