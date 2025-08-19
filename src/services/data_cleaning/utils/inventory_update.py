import json

import pandas as pd

from typing import Dict, Union

from src.services.utils.common_utils import CommonUtils
from config.constants import MAIN_PATH


class InventoryUpdate:
    def __init__(self, file: Union[str, pd.DataFrame, None] = None, dir_file: str = ""):
        self.file = file
        self.df: pd.DataFrame = CommonUtils(self.file, dir_file).convert_to_df() # type: ignore


    def update_single_row_name(self, column: str, old_name: str, new_name: str) -> pd.DataFrame:
        """ Updates a single row by an 'old_name' var to a 'new_name' in the column specified """

        self.df[column] = self.df[column].replace(old_name, new_name)
        
        self.df.to_excel(f"{MAIN_PATH}/out/{self.file}.xlsx", index=True)
        return self.df
    

    def update_column_by_dict(self, json_file: str) -> pd.DataFrame:
        """ Updates all the columns by the json file indicated. """
        with open(f"{MAIN_PATH}/src/data/json_data/{json_file}.json", "r", encoding="utf-8") as file:
            data: Dict[str, str] = json.load(file) 
       
        return self.df.rename(columns=data)


    def update_rows_by_dict(self, json_file: str, column: str) -> pd.DataFrame:
        """ Updates rows in the column specified by the json file indicated. """
        with open(f"{MAIN_PATH}/src/data/json_data/{json_file}.json", "r", encoding="utf-8") as file:
            data: Dict[str, str] = json.load(file)
        
        self.df[column] = self.df[column].replace(data)
        return self.df