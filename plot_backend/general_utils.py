import re
import glob
import os

import pandas as pd

from pathlib import Path
from typing import Union


class GeneralUtils:
    def __init__(self, file: Union[str, pd.DataFrame]) -> None:
        self.file = file
        self._main_path = Path.cwd()
        self._xls_files = glob.glob("**/*.xls", recursive=True)

    
    def check_filetype(self) -> pd.DataFrame:
        """
        Checks whereas the file entered is a string and converts it to dataframe \n
        and returns it or is already a dataframe and returns it.
        """
        if isinstance(self.file, str):
            df: pd.DataFrame = pd.read_excel(f"{self._main_path}/excel/{self.file}.xlsx", engine="calamine")
        else:
            df: pd.DataFrame = pd.DataFrame(self.file)
        
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


    @staticmethod
    def delete_error_bytes(string: str, eliminar: str) -> str:
        return re.sub(fr"{eliminar}", "", string)
    
