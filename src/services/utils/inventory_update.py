import json

import pandas as pd

from typing import Dict, Union, Optional

from services.utils.common_utils import CommonUtils
from services.utils.exception_utils import execute_safely
from config.constants import OUT_PATH, JSON_PATH


class InventoryUpdate:
    def __init__(self, file: Optional[Union[str, pd.DataFrame]] = None):
        self.file = file
        self.df: pd.DataFrame = CommonUtils()._convert_to_df(self.file) # type: ignore

    @execute_safely
    def _update_single_row_name(self, column: str, old_name: str, new_name: str) -> pd.DataFrame:
        """ Updates a single row by an 'old_name' var to a 'new_name' in the column specified """

        self.df[column] = self.df[column].replace(old_name, new_name)
        
        self.df.to_excel(f"{OUT_PATH}/{self.file}.xlsx", index=True)
        return self.df
    
    @execute_safely
    def _update_column_by_dict(self, json_file: str) -> pd.DataFrame:
        """ Updates all the columns by the json file indicated. """
        with open(f"{JSON_PATH}/{json_file}.json", "r", encoding="utf-8") as file:
            data: Dict[str, str] = json.load(file) 
       
        return self.df.rename(columns=data)

    @execute_safely
    def _update_rows_by_dict(self, json_file: str, column: str) -> pd.DataFrame:
        """ Updates rows in the column specified by the json file indicated. """
        with open(f"{JSON_PATH}/{json_file}.json", "r", encoding="utf-8") as file:
            data: Dict[str, str] = json.load(file)
        
        try:
            self.df[column] = self.df[column].replace(data)
        except KeyError:
            pass
        return self.df