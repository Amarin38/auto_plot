import pandas as pd

from datetime import date

from config.constants import MAIN_PATH
from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner
from services.analysis.maxmin.utils.maxmin_utils import MaxMinUtils

"""
- Se descargan los consumos de x fecha hacia atrás de los productos que se queira evaluar el  maxmin.
- Se procesa el file y quedan solo las salidas.
- Se pasa por el programa
"""

class MaxMin:
    def __init__(self, file: str, dir: str = "todo maxmin", 
                 multiplicar_por: float = 2.5, fecha: str = date.today().strftime("%d/%m/%Y")) -> None:
        self.dir = dir
        self.file = file      
        self.fecha = fecha
        self.multiplicar_por = multiplicar_por
        self.fecha_hoy = pd.Timestamp.today().strftime("%d-%m-%Y")

    
    def run_all(self) -> None:
        """
        Genera el file completo con los maxmin.
        """
        arreglar = InventoryDataCleaner(self.file, self.dir)
        arreglar.run_all()

        utils = MaxMinUtils(self.fecha, web=True)
        arreglar = InventoryDataCleaner(f"{self.file}-S")

        arreglar.filter("lista_codigos", utils.create_code_list(False))

        self.calculate()


    def calculate(self) -> None:
        """
        Calcula el nuevo minimo y maximo de cada repuesto y\n
        multiplica al minimo por el valor asignado. 
        """
        
        df: pd.DataFrame = pd.read_excel(f"{MAIN_PATH}/out/filtrado.xlsx", engine="calamine")

        df["FechaCompleta"] = pd.DatetimeIndex(pd.to_datetime(df["FechaCompleta"])).strftime("%Y-%m")
        fecha_max: pd.Timestamp = pd.to_datetime(df["FechaCompleta"].max()) + pd.Timedelta(days=30)
        fecha_rango_unico: pd.Index[str] = pd.date_range(df["FechaCompleta"].min(), fecha_max,freq="ME").unique().strftime("%Y-%m")

        df_agrupado: pd.DataFrame = df.groupby(["Familia", "Articulo", "Repuesto"]).agg({
            "Cantidad":"sum"
        }).reset_index()
        
        min_calc: pd.Series[float] = round(df_agrupado["Cantidad"]/len(fecha_rango_unico), 1)*self.multiplicar_por
        df_agrupado["Minimo"] = min_calc
        df_agrupado["Maximo"] = min_calc * 2
    
        df_agrupado = df_agrupado[["Familia", "Articulo", "Repuesto", "Minimo", "Maximo"]]

        df_agrupado.to_excel(f"{MAIN_PATH}/out/maxmin {self.fecha_hoy}.xlsx")
