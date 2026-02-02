import math
import re
import io
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, date
from zipfile import BadZipFile

import pandas as pd

from typing import List, Optional, Any

from statsmodels.graphics.tukeyplot import results
from streamlit.runtime.scriptrunner_utils.script_run_context import get_script_run_ctx, add_script_run_ctx


from config.constants_common import FILE_STRFTIME_DMY
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
                if isinstance(file, pd.DataFrame):
                    _xlsx_files.append(file)
                else:
                    try:
                        df = pd.read_excel(file, engine="openpyxl") # leo el xlsx
                    except BadZipFile:
                        df = pd.read_excel(file, engine="xlrd") # leo el xls
                    df = self.delete_unnamed_cols(df)

                    for col in df.columns:
                        df[col] = [self.delete_error_bytes(str(string), "\x00")
                                   if pd.notnull(string) else string for string
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


    @execute_safely
    def run_in_threads(self, functions, max_workers: Optional[int] = None) -> List[Any]:
        ctx = get_script_run_ctx()

        def run_with_context(func):
            def wrapper():
                if ctx:
                    add_script_run_ctx(thread=None, ctx=ctx)
                return func()
            return wrapper

        if max_workers is None:
            max_workers = len(functions)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            if isinstance(functions, list):
                futures = [executor.submit(run_with_context(func)) for func in functions] # ejecuto las funciones en los threads
                results = [future.result() for future in futures] # obtengo los resultados
            else:
                futures = executor.submit(run_with_context(functions))
                results = futures.result()
        return results

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


    # ------------------------------------------------------ PARSE ------------------------------------------------------
    @staticmethod
    def safe_int(value):
        if value is None:
            return None

        if isinstance(value, float) and math.isnan(value):
            return None

        if isinstance(value, str):
            value = value.strip()
            if value == "":
                return None

        try:
            return int(float(value))
        except (ValueError, TypeError):
            return None

    @staticmethod
    def safe_float(value):
        if value is None:
            return None

        if isinstance(value, int) and math.isnan(value):
            return None

        return float(value)

    @staticmethod
    def safe_date(value):
        if value is None:
            return None

            # NaN / NaT (pandas)
        if isinstance(value, float) and math.isnan(value):
            return None

        if pd.isna(value):
            return None

            # pandas Timestamp
        if isinstance(value, pd.Timestamp):
            return value.date()

            # datetime
        if isinstance(value, datetime):
            return value.date()

            # date
        if isinstance(value, date):
            return value

            # string
        if isinstance(value, str):
            value = value.strip()
            if value == "":
                return None
            try:
                return pd.to_datetime(value).date()
            except Exception:
                return None

        return None

    @execute_safely
    def num_parser(self, val) -> str:
        return (f"{val:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
                )

    @execute_safely
    def abreviar_es(self, n) -> str:
        if n >= 1_000_000_000:
            return f"{int(n / 1_000_000_000)} mil M"

        if n >= 1_000_000:
            return f"{int(n / 1_000_000)} M"

        if n >= 1_000:
            return f"{int(n / 1_000)} mil"

        return f"{int(n)}"