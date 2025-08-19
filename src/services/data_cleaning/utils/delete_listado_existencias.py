import pandas as pd

from typing import Union, Tuple

from services.utils.general_utils import GeneralUtils

class DeleteListadoExistencias:
    def __init__(self, file: Union[str, pd.DataFrame]) -> None:
        self.df: pd.DataFrame = GeneralUtils(file).convert_to_df() # type: ignore

    def delete_unnamed_cols(self) -> pd.DataFrame:
        """ Deletes all the 'Unnamed' columns. """
        self.df = self.df.loc[:, ~self.df.columns.str.contains("Unnamed")] 
        self.df = self.df.loc[:, ~self.df.columns.str.contains("Columna")]

        # self.df.to_excel(f"{MAIN_PATH}out/{self.file}.xlsx")
        return self.df


    def delete_rows(self, delete_type: str, delete_by: Tuple[str, ...]) -> pd.DataFrame:
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
                    self.df = self.df.loc[-self.df.Interno.str.contains(delete, na=False)]
            case _:
                return pd.DataFrame()
            
        # self.df.to_excel(f"{MAIN_PATH}/out/{self.file}.xlsx")
        return self.df