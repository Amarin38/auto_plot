import re
import glob
import os

import pandas as pd

from pathlib import Path
from typing import Union, Optional, List


class GeneralUtils:
    def __init__(self, file: Union[str, pd.DataFrame], xlsx_dir: Optional[str] = None) -> None:
        self.file = file
        self._xlsx_dir = xlsx_dir
        self._main_path = Path.cwd()
        self._xls_files = glob.glob("**/*.xls", recursive=True)
        self._xlsx_files = glob.glob(f"{self._main_path}/{self._xlsx_dir}/**/*.xlsx", recursive=True)

    def check_file_exists(self) -> bool:
        """
        Checks if the entered file name already exists.
        """
        return Path(f"{self._main_path}/excel/{self.file}.xlsx").exists()


    def check_filetype(self) -> pd.DataFrame:
        """
        Checks whereas the file entered is a string and converts it to dataframe \n
        and returns it or is already a dataframe and returns it.
        """
        try:
            if isinstance(self.file, str):
                df: pd.DataFrame = pd.read_excel(f"{self._main_path}/excel/{self.file}.xlsx", engine="calamine")
            else:
                df: pd.DataFrame = pd.DataFrame(self.file)
        except FileNotFoundError as e:
            print(f"No existe el archivo para checkear -> {e}")

        return df

    
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
            print(f"Ya existe el archivo {self.file}")
            return pd.DataFrame()
        else:
            self.xls_to_xlsx()
            df_list: List[str] = [] # type: ignore

            for file in self._xlsx_files:
                df_list.append(pd.read_excel(file, engine="calamine")) # type: ignore
            
            df_list: pd.DataFrame = pd.concat(df_list) # type: ignore

            return df_list
    

    @staticmethod
    def delete_error_bytes(string: str, eliminar: str) -> str:
        return re.sub(fr"{eliminar}", "", string)
    
