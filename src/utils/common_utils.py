import re
import io
from zipfile import BadZipFile

import pandas as pd

from typing import List, Tuple, Literal

from src.utils.exception_utils import execute_safely
from src.db_data.crud_common import read_json_config


class CommonUtils:
    @execute_safely
    def concat_dataframes(self, df_directory: List) -> pd.DataFrame:
        """
        Converts all the .xls files to .xlsx files and returns the concat of all of them\n
        """
        _xlsx_files = []
        if len(df_directory) != 0:
            for file in df_directory:
                try:
                    df = pd.read_excel(file, engine="openpyxl") # leo el xlsx
                except BadZipFile:
                    df = pd.read_excel(file, engine="xlrd") # leo el xls
                df = self.del_unnamed_cols(df)

                buffer = io.BytesIO()
                df.to_excel(buffer, index=False, engine="openpyxl")
                buffer.seek(0) # muevo el puntero a la primera posicion otra vez

                _xlsx_files.append(df)
            
            df = pd.concat(_xlsx_files)

            if "pronom" in df.columns:
                df["pronom"] = [self.del_error_bytes(str(string), "\x00") if pd.notnull(string) else string for string in df["pronom"]]

            return df
        return pd.DataFrame()
    

    # ------------------------------------------------------ DELETE ------------------------------------------------------
    @staticmethod
    @execute_safely
    def del_unnamed_cols(df: pd.DataFrame) -> pd.DataFrame:
        """ Deletes all the 'Unnamed' columns. """
        if df.columns.str.contains("Unnamed").any():
            df = df.loc[:, ~df.columns.str.contains("Unnamed")] 
            df = df.loc[:, ~df.columns.str.contains("Columna")]

        return df


    @staticmethod
    @execute_safely
    def del_by_content(df: pd.DataFrame, column: str, delete_by: Tuple[str, ...]):
        delete = "|".join(delete_by)
        df[column] = df[column].fillna("").astype(str)

        return df.loc[~df[column].str.contains(delete, na=False)] # guardo indices de los elementos para borrar    


    @staticmethod
    def del_error_bytes(string: str, eliminar: str) -> str:
        return re.sub(fr"{eliminar}", "", string)


    # ------------------------------------------------------ UPDATE ------------------------------------------------------
    @staticmethod
    @execute_safely
    def upd_single_row_name(df: pd.DataFrame, column: str, old_name: str, new_name: str) -> pd.DataFrame:
        """ Updates a single row by an 'old_name' var to a 'new_name' in the column specified """
        df[column] = df[column].replace(old_name, new_name)
        return df
        

    @staticmethod
    @execute_safely
    def upd_column_by_dict(df: pd.DataFrame, json_col: str) -> pd.DataFrame:
        """ Updates all the columns by the json file indicated. """
        return df.rename(columns=read_json_config(json_col))


    @staticmethod
    @execute_safely
    def upd_rows_by_dict(df: pd.DataFrame, json_col: str, column: str) -> pd.DataFrame:
        """ Updates rows in the column specified by the json file indicated. """
        df[column] = df[column].replace(read_json_config(json_col))
        return df


    # def _convert_xls_to_xlsx(self, directory) -> None:
    #     """
    #     Converts all the .xls files in the current directoryectory into a fully working .xlsx file\n
    #     deleting all the errors within the out .xls file.
    #     """
    #     _xls_files = glob.glob(f"{MAIN_PATH}/{directory}/**/*.xls", recursive=True)
        
    #     for file in _xls_files:
    #         file_mod_name = file.replace(".xls", "")

    #         try:
    #             df: pd.DataFrame = pd.read_excel(file, engine="xlrd")
    #             df["pronom"] = [self._delete_error_bytes(str(string), "\x00") if pd.notnull(string) else string for string in df["pronom"]]
    #             df.to_excel(f"{file_mod_name}.xlsx")
    #         except AssertionError:
    #             sheet = pe.get_sheet(file_name=file)
    #             sheet.save_as(file_mod_name)

    #         os.remove(file)


    # @execute_safely
    # def append_df(self, directory: str, save: Literal["SAVE", "NOT SAVE"] = "NOT SAVE") -> pd.DataFrame:
    #     """
    #     Appends all the xlsx files into one single file with 
    #     the name entered. 
    #     """
    #     self._convert_xls_to_xlsx(directory)
    #     _xlsx_files = glob.glob(f"{MAIN_PATH}/{directory}/**/*.xlsx", recursive=True)

    #     if len(_xlsx_files) != 0:
    #         df_list: pd.DataFrame = pd.concat([pd.read_excel(file, engine="calamine") for file in _xlsx_files])
            
    #         return df_list
    #     return pd.DataFrame()
    

