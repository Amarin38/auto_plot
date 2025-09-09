import re
import glob
import os

import pandas as pd
import pyexcel as pe

from pathlib import Path
from typing import Union, Any, Literal

from src.config.constants import MAIN_PATH, OUT_PATH
from src.services.utils.exception_utils import execute_safely
from src.config.enums import SaveEnum

class CommonUtils:
    @staticmethod
    @execute_safely
    def check_file_exists(path: Path, file: str) -> bool:
        """
        Checks if the entered file name already exists.
        """
        return Path(f"{path}/{file}.xlsx").exists()


    @staticmethod
    @execute_safely
    def convert_to_df(file: Union[str, Any]) -> pd.DataFrame:
        """
        Checks whereas the file entered is a string and converts it to dataframe \n
        and returns it or is already a dataframe and returns it.
        """
        if isinstance(file, str):
            return pd.read_excel(f"{OUT_PATH}/{file}.xlsx", engine="calamine")
        else:
            return pd.DataFrame(file)


    def _convert_xls_to_xlsx(self, directory) -> None:
        """
        Converts all the .xls files in the current directoryectory into a fully working .xlsx file\n
        deleting all the errors within the out .xls file.
        """
        _xls_files = glob.glob(f"{MAIN_PATH}/{directory}/**/*.xls", recursive=True)
        
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


    @execute_safely
    def append_df(self, directory: str, save: Literal["GUARDAR", "NO GUARDAR"] = "NO GUARDAR") -> pd.DataFrame:
        """
        Appends all the xlsx files into one single file with 
        the name entered. 
        """
        self._convert_xls_to_xlsx(directory)
        _xlsx_files = glob.glob(f"{MAIN_PATH}/{directory}/**/*.xlsx", recursive=True)

        if len(_xlsx_files) != 0:
            df_list: pd.DataFrame = pd.concat([pd.read_excel(file, engine="calamine") for file in _xlsx_files])
            
            if save == SaveEnum.SAVE.value:
                df_list.to_excel(f"{OUT_PATH}/appended_df.xlsx", index=False)
            return df_list
        return pd.DataFrame()
    

    @staticmethod
    def _delete_error_bytes(string: str, eliminar: str) -> str:
        return re.sub(fr"{eliminar}", "", string)