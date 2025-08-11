import json

import pandas as pd
import numpy as np

from typing import Dict, Union
from pathlib import Path

from plot_backend.general_utils import GeneralUtils


class UpdateListadoExistencias:
    def __init__(self, file: Union[str, pd.DataFrame]):
        self.file = file
        self.df = GeneralUtils(file).check_filetype()
        self._main_path = Path.cwd()


    def update_single_row_name(self, column: str, old_name: str, new_name: str) -> pd.DataFrame:
        """ Updates a single row by an 'old_name' var to a 'new_name' in the column specified """

        self.df[column] = self.df[column].replace(old_name, new_name)
        
        self.df.to_excel(f"{self._main_path}/excel/{self.file}.xlsx", index=True)
        return self.df
    

    def update_column_by_dict(self, json_file: str) -> pd.DataFrame:
        " Updates all the columns by the json file indicated"
        with open(f"json/{json_file}.json", "r", encoding="utf-8") as file:
            data: Dict[str, str] = json.load(file) 
       
        return self.df.rename(columns=data)


    def update_rows_by_dict(self, json_file: str, column: str ) -> pd.DataFrame:
        """ Updates rows in the column specified by the json file indicated. """
        with open(f"json/{json_file}.json", "r", encoding="utf-8") as file:
            data: Dict[str, str] = json.load(file)
        
        self.df[column] = self.df[column].replace(data)
        return self.df


class DeleteListadoExistencias:
    def __init__(self, file: Union[str, pd.DataFrame]) -> None:
        self.df = GeneralUtils(file).check_filetype()
        self._main_path = Path.cwd()

    def delete_unnamed_cols(self) -> pd.DataFrame:
        """ Deletes all the 'Unnamed' columns. """
        self.df = self.df.loc[:, ~self.df.columns.str.contains("Unnamed")]
        self.df = self.df.loc[:, ~self.df.columns.str.contains("Columna")]

        # self.df.to_excel(f"{self._main_path}excel/{self.file}.xlsx")
        return self.df


    def delete_rows(self, delete_type: str, delete_by: np.ndarray) -> pd.DataFrame:
        """
        Deletes the row by entered string.\n
        Delete types: repuesto, fechacompleta.\n
        Delete by: (np.ndarray)
        """
        match delete_type:
            case "repuesto":
                for delete in delete_by:
                    self.df = self.df.loc[~self.df.Repuesto.str.contains(delete, na=False)] # guardo indices de los elementos para borrar
            case "fechacompleta":
                for delete in delete_by:
                    self.df = self.df.loc[~self.df.FechaCompleta.str.contains(delete, na=False)]
            case "interno":
                for delete in delete_by:
                    self.df = self.df.loc[~self.df.Interno.str.contains(delete, na=False)]
            case _:
                return pd.DataFrame()
            
        # self.df.to_excel(f"{self._main_path}/excel/{self.file}.xlsx")
        return self.df