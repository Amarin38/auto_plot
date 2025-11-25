import re
import io
from zipfile import BadZipFile

import pandas as pd

from typing import List

from config.constants import FILE_STRFTIME_DMY
from utils.exception_utils import execute_safely
from viewmodels.common.json_config_vm import JSONConfigVM


class CommonUtils:
    @execute_safely
    def concat_dataframes(self, df_directory: List) -> pd.DataFrame:
        """
        Converts all the .xls files to .xlsx files and returns the concat of all of them\n
        """
        _xlsx_files = []
        if df_directory is not None:


            for file in df_directory:
                try:
                    df = pd.read_excel(file, engine="openpyxl") # leo el xlsx
                except BadZipFile:
                    df = pd.read_excel(file, engine="xlrd") # leo el xls
                df = self.delete_unnamed_cols(df)

                for col in df.columns:
                    df[col] = [self.delete_error_bytes(str(string), "\x00") if pd.notnull(string) else string for string
                               in df[col]]

                buffer = io.BytesIO()
                df.to_excel(buffer, index=False, engine="openpyxl")
                buffer.seek(0) # muevo el puntero a la primera posicion otra vez

                _xlsx_files.append(df)
            
            df = pd.concat(_xlsx_files)

            return df
        return pd.DataFrame()


    @execute_safely
    def to_excel(self, df: pd.DataFrame) -> bytes:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:  # type: ignore
            df.to_excel(writer, index=False, sheet_name="Datos")
        return output.getvalue()


    @execute_safely
    def devolver_fecha(self, df: pd.DataFrame, columna: str) -> str:
        if df.size == 0:
            return ""
        return pd.to_datetime(df[columna].unique()).strftime(FILE_STRFTIME_DMY)[0]

    # ------------------------------------------------------ DELETE ------------------------------------------------------
    @staticmethod
    @execute_safely
    def delete_unnamed_cols(df: pd.DataFrame) -> pd.DataFrame:
        """ Deletes all the 'Unnamed' columns. """
        if df.columns.str.contains("Unnamed").any():
            df = df.loc[:, ~df.columns.str.contains("Unnamed")] 
            df = df.loc[:, ~df.columns.str.contains("Columna")]

        return df


    @staticmethod
    @execute_safely
    def delete_by_content(df: pd.DataFrame, column: str, delete_by: List[str]):
        delete = "|".join(delete_by)
        df[column] = df[column].fillna("").astype(str)

        return df.loc[~df[column].str.contains(delete, na=False)] # guardo indices de los elementos para borrar    


    @staticmethod
    def delete_error_bytes(string: str, eliminar: str) -> str:
        return re.sub(fr"{eliminar}", "", string)


    # ------------------------------------------------------ UPDATE ------------------------------------------------------
    @staticmethod
    @execute_safely
    def update_single_row_name(df: pd.DataFrame, column: str, old_name: str, new_name: str) -> pd.DataFrame:
        """ Updates a single row by an 'old_name' var to a 'new_name' in the column specified """
        df[column] = df[column].replace(old_name, new_name)
        return df
        

    @staticmethod
    @execute_safely
    def update_columns(df: pd.DataFrame, json_col: str) -> pd.DataFrame:
        """ Updates all the columns by the json file indicated. """
        return df.rename(
            columns=JSONConfigVM().get_df_by_id(json_col)
        )


    @staticmethod
    @execute_safely
    def update_rows_by_dict(df: pd.DataFrame, json_col: str, column: str) -> pd.DataFrame:
        """ Updates rows in the column specified by the json file indicated. """
        df[column] = df[column].replace(
            JSONConfigVM().get_df_by_id(json_col)
        )
        return df

