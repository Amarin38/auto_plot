import pandas as pd

from typing import Union, Tuple

from src.services.utils.common_utils import CommonUtils
from src.services.utils.exception_utils import execute_safely

class InventoryDelete:
    def __init__(self, file: Union[str, pd.DataFrame]) -> None:
        self.df: pd.DataFrame = CommonUtils().convert_to_df(file) # type: ignore

    @execute_safely
    def delete_unnamed_cols(self) -> pd.DataFrame:
        """ Deletes all the 'Unnamed' columns. """
        if self.df.columns.str.contains("Unnamed").any():
            self.df = self.df.loc[:, ~self.df.columns.str.contains("Unnamed")] 
            self.df = self.df.loc[:, ~self.df.columns.str.contains("Columna")]

        return self.df


    @execute_safely
    def delete_repuestos(self, delete_by: Tuple[str, ...]) -> pd.DataFrame:
        delete = "|".join(delete_by)
        return self.df.loc[~self.df.Repuesto.str.contains(delete, na=False)] # guardo indices de los elementos para borrar


    @execute_safely
    def delete_fecha(self, delete_by: Tuple[str, ...]) -> pd.DataFrame:
        delete = "|".join(delete_by)
        return self.df.loc[~self.df.FechaCompleta.str.contains(delete, na=False)] # TODO: modificar para que elimine por date y no por str
    

    @execute_safely
    def delete_interno(self, delete_by: Tuple[str, ...]) -> pd.DataFrame:
        delete = "|".join(delete_by)
        return self.df.loc[~self.df.Interno.str.contains(delete, na=False)]
