import pandas as pd
from pathlib import Path
from io import BytesIO

from src.config.constants import MAIN_PATH
from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner
from src.services.utils.maxmin_utils import MaxMinUtils
from src.services.utils.exception_utils import execute_safely
from src.db.crud import df_to_sql, sql_to_df
from src.services.utils.common_utils import CommonUtils

"""
- Se descargan los consumos de x fecha hacia atrás de los productos que se queira evaluar el  maxmin.
- Se procesa el file y quedan solo las salidas.
- Se pasa por el programa
"""

class MaxMin:
    def __init__(self) -> None:
        self.utils = MaxMinUtils()
        self.data_cleaner = InventoryDataCleaner()
        self.common = CommonUtils()
    
    @execute_safely
    def create_maxmin(self, directory: str = "todo maxmin") -> pd.DataFrame:
        # if self.common.check_file_exists(MAIN_PATH, directory):
        # self.utils.create_code_list("08/09/2025")
        # return self.calculate()
        # else:
        return sql_to_df("maxmin")


    @execute_safely
    def calculate(self, directory: str = "todo maxmin", multiplicar_por: float = 2.5) -> pd.DataFrame:
        df = self.data_cleaner.run_all(directory)
        
        df_agrupado: pd.DataFrame = df.groupby(["Familia", "Articulo", "Repuesto"]).agg({"Cantidad":"sum"}).reset_index()
        min_calc: pd.Series[float] = round(df_agrupado["Cantidad"] / 6, 1) * multiplicar_por

        df_agrupado["Minimo"] = min_calc
        df_agrupado["Maximo"] = min_calc * 2
    
        df_agrupado = df_agrupado[["Familia", "Articulo", "Repuesto", "Minimo", "Maximo"]]

        df_to_sql("maxmin", df_agrupado)
        return df_agrupado


    @execute_safely
    def to_excel(self, df: pd.DataFrame):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Datos")
        return output.getvalue()
    