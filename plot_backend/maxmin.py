import pandas as pd

from numpy import ndarray
from typing import Dict, List, Union

from plot_backend.constants import MAIN_PATH
from plot_backend.utils_maxmin import UtilsMaxMin

"""
- Se descargan los consumos de x fecha hacia atrás de los productos que se queira evaluar el  maxmin.
- Se procesa el archivo y quedan solo las salidas.
- Se pasa por el programa
"""

class MaxMin:
    def __init__(self, file: str, multiplicar_por: float) -> None:
        self.multiplicar_por = multiplicar_por

        self.base_df = pd.read_excel(f"{MAIN_PATH}/excel/{file}.xlsx", engine="calamine")
        self.df = self._fecha_completa_a_mes() 
        self.fecha_hoy = pd.Timestamp.today().strftime("%d-%m-%Y")


    def calcular(self) -> None:
        """
        Calcula el nuevo minimo y maximo de cada repuesto y\n
        multiplica al minimo por el valor asignado. 
        """

        lista_totales_mes: List[Dict[str, Union[str, float, int, pd.Timestamp]]] = []
        lista_totales_rep: List[Dict[str, Union[str, float, int, pd.Timestamp]]] = []
        repuestos: ndarray = self.df["Repuesto"].unique()

        fecha_rango_unico = pd.date_range(self.df["FechaCompleta"].min(), 
                                          self.df["FechaCompleta"].max(), freq="ME").unique().strftime("%Y-%m")
        
        for repuesto in repuestos:
            fam_rep = self.df.loc[self.df["Repuesto"] == repuesto, ["Familia"]].iloc[0].values[0]
            art_rep = self.df.loc[self.df["Repuesto"] == repuesto, ["Articulo"]].iloc[0].values[0]

            total_repuesto_final: int = 0
            for fecha in fecha_rango_unico:
                total_repuesto_mes = self.df.loc[(self.df["Repuesto"] == repuesto) &
                                                 (self.df["FechaCompleta"] == fecha),
                                                 "Cantidad"].sum() # type: ignore
                
                total_repuesto_final += total_repuesto_mes

                lista_totales_mes.append({ # type: ignore
                    "Familia":fam_rep, # type: ignore
                    "Articulo":art_rep,
                    "Repuesto":repuesto,
                    "FechaCompleta":fecha,
                    "TotalMes":total_repuesto_mes
                })

            minimo = round(total_repuesto_final/len(fecha_rango_unico), 1)
            lista_totales_rep.append({#type: ignore
                " ":"", # espacio entre las tablas
                "Familia":fam_rep, 
                "Articulo":art_rep,
                "RepuestoUnico":repuesto,
                "Minimo": minimo*self.multiplicar_por,
                "Maximo": minimo*(self.multiplicar_por*2)
            })

        df_final = pd.concat((pd.DataFrame(lista_totales_mes), pd.DataFrame(lista_totales_rep)), axis=1) # type: ignore
        df_final.to_excel(f"{MAIN_PATH}/excel/maxmin {self.fecha_hoy}.xlsx")


    def _fecha_completa_a_mes(self) -> pd.DataFrame:
        """ Genero un dataframe nuevo con la fecha modificada en formato %Y-%m """

        self.base_df["FechaCompleta"] = pd.DatetimeIndex(pd.to_datetime(self.base_df["FechaCompleta"])).strftime("%Y-%m")
        return self.base_df

