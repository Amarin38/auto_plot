import json

import pandas as pd

from typing import Dict, Union

from src.services.utils.common_utils import CommonUtils
from src.services.utils.exception_utils import execute_safely
from src.config.constants import OUT_PATH, JSON_PATH
from src.config.enums import SaveEnum


class InventoryUpdate:
    @staticmethod
    @execute_safely
    def single_row_name(file: Union[str, pd.DataFrame], column: str, old_name: str, new_name: str, save: str = "NO GUARDAR") -> pd.DataFrame:
        """ Updates a single row by an 'old_name' var to a 'new_name' in the column specified """
        df = CommonUtils().convert_to_df(file)
        
        df[column] = df[column].replace(old_name, new_name)

        if save == SaveEnum.SAVE.value:
            df.to_excel(f"{OUT_PATH}/{file}.xlsx", index=True)
        return df
    
    @staticmethod
    @execute_safely
    def column_by_dict(file: Union[str, pd.DataFrame], json_file: str) -> pd.DataFrame:
        """ Updates all the columns by the json file indicated. """
        df = CommonUtils().convert_to_df(file)

        with open(f"{JSON_PATH}/{json_file}.json", "r", encoding="utf-8") as f:
            data: Dict[str, str] = json.load(f) 
       
        return df.rename(columns=data)

    @staticmethod
    @execute_safely
    def rows_by_dict(file: Union[str, pd.DataFrame], json_file: str, column: str) -> pd.DataFrame:
        """ Updates rows in the column specified by the json file indicated. """
        df = CommonUtils().convert_to_df(file)

        with open(f"{JSON_PATH}/{json_file}.json", "r", encoding="utf-8") as f:
            data: Dict[str, str] = json.load(f)
        
        df[column] = df[column].replace(data)
        return df