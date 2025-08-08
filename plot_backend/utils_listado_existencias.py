import json
import pandas as pd
import numpy as np

from pathlib import Path
from typing import Dict, Union, List


class UtilsListadoExistencias:
    def __init__(self, file: str):
        self.file = file
        self._main_path = Path.cwd()


    # --- UPDATE --- #
    def update_single_row_name(self, xlsx_file: str, column: str, old_name: str, new_name: str) -> pd.DataFrame:
        """ Updates a single row by an 'old_name' var to a 'new_name' in the column specified """
        utils = GeneralUtils(xlsx_file)
        df: pd.DataFrame = utils.check_filetype()

        df[column] = df[column].replace(old_name, new_name)
        
        df.to_excel(f"{self._main_path}/excel/{self.file}.xlsx", index=True)
        return df


    def update_column_by_dict(self, xlsx_file: Union[str, pd.DataFrame], archivo_json: str) -> pd.DataFrame:
        " Updates all the columns by the json file indicated"
        with open(f"json/{archivo_json}.json", "r", encoding="utf-8") as file:
            data: Dict[str, str] = json.load(file) 
       
        utils = GeneralUtils(xlsx_file)
        df: pd.DataFrame = utils.check_filetype()
        return df.rename(columns=data)


    def update_rows_by_dict(self, xlsx_file: Union[str, pd.DataFrame], json_file: str, column: str ) -> pd.DataFrame:
        """ Updates rows in the column specified by the json file indicated. """
        with open(f"json/{json_file}.json", "r", encoding="utf-8") as file:
            data: Dict[str, str] = json.load(file)
        
        utils = GeneralUtils(xlsx_file)
        df: pd.DataFrame = utils.check_filetype()
        df[column] = df[column].replace(data)
        return df


    # --- DELETE --- #
    def delete_unnamed_cols(self, df: Union[str, pd.DataFrame]) -> pd.DataFrame:
        """ Deletes all the 'Unnamed' columns. """

        utils = GeneralUtils(df)
        df_limpio: pd.DataFrame = utils.check_filetype()
        df_limpio = df_limpio.loc[:, ~df_limpio.columns.str.contains("Unnamed")]
        df_limpio = df_limpio.loc[:, ~df_limpio.columns.str.contains("Columna")]

        # df_limpio.to_excel(f"{self._main_path}excel/{self.file}.xlsx")
        return df_limpio


    def delete_rows(self, delete_type: str, delete_by: np.ndarray) -> pd.DataFrame:
        """
        Deletes the row by entered string.\n
        Delete types: repuesto, fechacompleta.\n
        Delete by: np.ndarray
        """
        utils = GeneralUtils(self.file)
        df: pd.DataFrame = utils.check_filetype()

        match delete_type:
            case "repuesto":
                for delete in delete_by:
                    df = df.loc[-df.Repuesto.str.contains(delete, na=False)] # guardo indices de los elementos para borrar
            case "fechacompleta":
                for delete in delete_by:
                    df = df.loc[-df.FechaCompleta.str.contains(delete, na=False)]
            case "interno":
                for delete in delete_by:
                    df = df.loc[-df.Interno.str.contains(delete, na=False)]
            case _:
                return  pd.DataFrame()
        
        # df.to_excel(f"{self._main_path}/excel/{self.file}.xlsx")
        return df


    def separar_internos_cabecera(self) -> pd.DataFrame:
        utils = GeneralUtils(self.file)
        df: pd.DataFrame = utils.check_filetype()

        cabeceras = df["Cabecera"].unique()

        list_internos: List[Dict[str, int]] = []

        for cab in cabeceras:
            internos_cabecera: List[int] = df.loc[df["Cabecera"] == cab, "Interno"].dropna().unique().tolist() # type: ignore

            for inter in internos_cabecera:
                list_internos.append({
                    "Cabecera":cab,
                    "Interno":inter
                })

        df_internos: pd.DataFrame = pd.DataFrame(list_internos)
        df_internos.to_excel("internos_cabecera.xlsx")
        return df
    

class GeneralUtils:
    def __init__(self, file: Union[str, pd.DataFrame]) -> None:
        self.file = file
        self._main_path = Path.cwd()
    
    def check_filetype(self):
        """
        Checks whereas the file entered is a string and converts it to dataframe \n
        and returns it or is already a dataframe and returns it.
        """
        if isinstance(self.file, str):
            df: pd.DataFrame = pd.read_excel(f"excel/{self.file}.xlsx", engine="calamine")
        else:
            df: pd.DataFrame = pd.DataFrame(self.file)
        
        return df