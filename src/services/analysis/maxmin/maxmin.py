import pandas as pd

from numpy import ndarray
from datetime import date
from typing import Dict, List, Union

from config.constants import MAIN_PATH
from services.data_cleaning.listado_existencias import ArreglarListadoExistencias
from services.analysis.maxmin.utils.maxmin_utils import MaxMinUtils

"""
- Se descargan los consumos de x fecha hacia atrás de los productos que se queira evaluar el  maxmin.
- Se procesa el archivo y quedan solo las salidas.
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

    
    def generar_maxmin_completo(self) -> None:
        """
        Genera el archivo completo con los maxmin.
        """
        arreglar = ArreglarListadoExistencias(self.file, self.dir)
        arreglar.arreglar_listado()

        utils = MaxMinUtils(self.fecha, web=True)
        arreglar = ArreglarListadoExistencias(f"{self.file}-S")

        arreglar.filter("lista_codigos", utils.generar_lista_codigos(False))

        self.calcular()


    def calcular(self) -> None:
        """
        Calcula el nuevo minimo y maximo de cada repuesto y\n
        multiplica al minimo por el valor asignado. 
        """
        
        df = pd.read_excel(f"{MAIN_PATH}/out/filtrado.xlsx", engine="calamine")
        df["FechaCompleta"] = pd.DatetimeIndex(pd.to_datetime(df["FechaCompleta"])).strftime("%Y-%m")

        fecha_max = pd.to_datetime(df["FechaCompleta"].max()) + pd.Timedelta(days=30)
        fecha_rango_unico = pd.date_range(df["FechaCompleta"].min(), fecha_max,freq="ME").unique().strftime("%Y-%m")


        df_agrupado = df.groupby(["Familia", "Articulo", "Repuesto"]).agg({
            "Cantidad":"sum"
        }).reset_index()
        
        min_calc = round(df_agrupado["Cantidad"]/len(fecha_rango_unico), 1)*self.multiplicar_por
        df_agrupado["Minimo"] = min_calc
        df_agrupado["Maximo"] = min_calc * 2

        df_agrupado = df_agrupado[["Familia", "Articulo", "Repuesto", "Minimo", "Maximo"]]

        df_agrupado.to_excel(f"{MAIN_PATH}/out/maxmin {self.fecha_hoy}.xlsx")
