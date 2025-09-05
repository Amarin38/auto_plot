import pandas as pd

from src.config.constants import OUT_PATH, TODAY_DATE_PAGE, TODAY_DATE_FILE
from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner
from src.services.utils.maxmin_utils import MaxMinUtils
from src.services.utils.exception_utils import execute_safely

"""
- Se descargan los consumos de x fecha hacia atrás de los productos que se queira evaluar el  maxmin.
- Se procesa el file y quedan solo las salidas.
- Se pasa por el programa
"""

class MaxMin:
    def __init__(self, file: str, directory: str = "todo maxmin", date_since: str = TODAY_DATE_PAGE) -> None:
        self.file = file
        self.directory = directory
        self.date_since = date_since


    @execute_safely
    def prepare_data(self) -> pd.DataFrame:
        """
        Calcula el nuevo minimo y maximo de cada repuesto y\n
        multiplica al minimo por el valor asignado. 
        """
        df = InventoryDataCleaner(self.file, self.directory).run_all()
        return InventoryDataCleaner(df).filter_lista_codigos(MaxMinUtils().create_code_list(self.date_since)) # type: ignore
        


    @execute_safely
    def calculate(self, multiplicar_por: float = 2.5):
        df = self.prepare_data()

        # --- Fechas --- #
        fecha_max: pd.Timestamp = df["FechaCompleta"].max()
        fecha_min: pd.Timestamp = df["FechaCompleta"].min()
        fecha_rango_unico = pd.date_range(fecha_min, fecha_max, freq="ME").unique()
        
        df_agrupado: pd.DataFrame = df.groupby(["Familia", "Articulo", "Repuesto"]).agg({"Cantidad":"sum"}).reset_index()
        
        min_calc: pd.Series[float] = round(df_agrupado["Cantidad"] / len(fecha_rango_unico), 1) * multiplicar_por
        df_agrupado["Minimo"] = min_calc
        df_agrupado["Maximo"] = min_calc * 2
    
        df_agrupado = df_agrupado[["Familia", "Articulo", "Repuesto", "Minimo", "Maximo"]]

        df_agrupado.to_excel(f"{OUT_PATH}/maxmin {TODAY_DATE_FILE}.xlsx")
