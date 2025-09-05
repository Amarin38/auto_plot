import pandas as pd

from typing import Union, Tuple

from src.services.utils.common_utils import CommonUtils
from src.services.utils.exception_utils import execute_safely

class InventoryDelete:
    @execute_safely
    def unnamed_cols(self, file: Union[str, pd.DataFrame]) -> pd.DataFrame:
        """ Deletes all the 'Unnamed' columns. """
        df = CommonUtils().convert_to_df(file)

        if df.columns.str.contains("Unnamed").any():
            df = df.loc[:, ~df.columns.str.contains("Unnamed")] 
            df = df.loc[:, ~df.columns.str.contains("Columna")]

        return df


    @execute_safely
    def by_content(self, file: Union[str, pd.DataFrame], column: str, delete_by: Tuple[str, ...]):
        df = CommonUtils().convert_to_df(file)

        delete = "|".join(delete_by)
        return df.loc[~df[column].str.contains(delete, na=False)] # guardo indices de los elementos para borrar

