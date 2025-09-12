import pandas as pd

from typing import Union, Literal

from src.services.utils.common_utils import CommonUtils
from src.services.utils.exception_utils import execute_safely
from src.config.constants import OUT_PATH
from src.config.enums import SaveEnum
from src.db.crud import read_json_config

class InventoryUpdate:
    def __init__(self) -> None:
        self.common = CommonUtils()

    @execute_safely
    def single_row_name(self, file: Union[str, pd.DataFrame], column: str, old_name: str, new_name: str, save: Literal["SAVE", "NOT SAVE"] = "NOT SAVE") -> pd.DataFrame:
        """ Updates a single row by an 'old_name' var to a 'new_name' in the column specified """
        df = self.common.convert_to_df(file)
        
        df[column] = df[column].replace(old_name, new_name)

        if save == SaveEnum.SAVE.value:
            df.to_excel(f"{OUT_PATH}/{file}.xlsx", index=True)
        return df
    

    @execute_safely
    def column_by_dict(self, file: Union[str, pd.DataFrame], json_col: str) -> pd.DataFrame:
        """ Updates all the columns by the json file indicated. """
        df = self.common.convert_to_df(file)
        return df.rename(columns=read_json_config(json_col))


    @execute_safely
    def rows_by_dict(self, file: Union[str, pd.DataFrame], json_col: str, column: str) -> pd.DataFrame:
        """ Updates rows in the column specified by the json file indicated. """
        df = self.common.convert_to_df(file)
        df[column] = df[column].replace(read_json_config(json_col))
        return df