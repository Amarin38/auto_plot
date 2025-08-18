import pandas as pd

from numpy import ndarray
from datetime import date
from typing import Dict, List, Union

from src.config import MAIN_PATH
from src.services import ArreglarListadoExistencias
from src.services import MaxMinUtils

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
        self.df = self._convertir_fecha_completa_a_mes(pd.read_excel(f"{MAIN_PATH}/out/filtrado.xlsx", engine="calamine")) 

        self.calcular()


    def calcular(self) -> None:
        """
        Calcula el nuevo minimo y maximo de cada repuesto y\n
        multiplica al minimo por el valor asignado. 
        """

        lista_totales_mes: List[Dict[str, Union[str, float, int, pd.Timestamp]]] = []
        lista_totales_rep: List[Dict[str, Union[str, float, int, pd.Timestamp]]] = []
        repuestos: ndarray = self.df["Repuesto"].unique()

        fecha_max = pd.to_datetime(self.df["FechaCompleta"].max()) + pd.Timedelta(days=30)
        fecha_rango_unico = pd.date_range(self.df["FechaCompleta"].min(), fecha_max,freq="ME").unique().strftime("%Y-%m")

        for repuesto in repuestos:
            fam_rep = self.df.loc[self.df["Repuesto"] == repuesto, ["Familia"]].iloc[0].values[0]
            art_rep = self.df.loc[self.df["Repuesto"] == repuesto, ["Articulo"]].iloc[0].values[0]

            total_repuesto_final: int = 0
            for fecha in fecha_rango_unico:
                total_repuesto_mes = self.df.loc[(self.df["Repuesto"] == repuesto) &
                                                 (self.df["FechaCompleta"] == fecha),
                                                 "Cantidad"].sum() # type: ignore
                
                total_repuesto_final += total_repuesto_mes

                lista_totales_mes.append({
                    "Familia":fam_rep,
                    "Articulo":art_rep,
                    "Repuesto":repuesto,
                    "FechaCompleta":fecha,
                    "TotalMes":total_repuesto_mes
                })

            minimo = round(total_repuesto_final/len(fecha_rango_unico), 1)
            lista_totales_rep.append({
                " ":"",
                "Familia":fam_rep, 
                "Articulo":art_rep,
                "RepuestoUnico":repuesto,
                "Minimo": minimo*self.multiplicar_por,
                "Maximo": minimo*(self.multiplicar_por*2)
            })

        df_final = pd.concat((pd.DataFrame(lista_totales_mes), pd.DataFrame(lista_totales_rep)), axis=1)
        df_final.to_excel(f"{MAIN_PATH}/out/maxmin {self.fecha_hoy}.xlsx")


    def _convertir_fecha_completa_a_mes(self, base_df) -> pd.DataFrame:
        """ Genero un dataframe nuevo con la fecha modificada en formato %Y-%m """

        base_df["FechaCompleta"] = pd.DatetimeIndex(pd.to_datetime(base_df["FechaCompleta"])).strftime("%Y-%m")
        return base_df

