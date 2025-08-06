import pandas as pd

from pathlib import Path
from numpy import ndarray
from typing import Dict, List, Union

class MaxMin:
    def __init__(self, archivo: str, multiplicar_por: float) -> None:
        self._main_path = Path.cwd()
        self.df = self.transformar_fecha_completa_a_fecha_mes(pd.read_excel(f"{self._main_path}/excel/{archivo}-S.xlsx", engine="calamine")) 
        self.mult_por = multiplicar_por
        self.fecha_hoy = pd.Timestamp.today().strftime("%d-%m-%Y")

    def calcular_max_min(self) -> None:
        lista_totales_mes: List[Dict[str, Union[str, float, int, pd.Timestamp]]]= []
        lista_totales_rep: List[Dict[str, Union[str, float, int, pd.Timestamp]]]= []
        repuestos: ndarray = self.df["Repuesto"].unique()

        # Fechas
        fecha_rango_unico = pd.date_range(self.df["FechaCompleta"].min(), 
                                          self.df["FechaCompleta"].max(), freq="ME").unique().strftime("%Y-%m")
        
        for rep in repuestos:
            cod_rep = self.df.loc[self.df["Repuesto"] == rep, ["Codigo"]].iloc[0].values[0]# type: ignore

            total_repuesto_final: int = 0
            for fecha in fecha_rango_unico:
                total_repuesto_mes = self.df.loc[(self.df["Repuesto"] == rep) &
                                            (self.df["FechaCompleta"] == fecha),
                                            "Cantidad"].sum() # type: ignore
                
                total_repuesto_final += total_repuesto_mes

                lista_totales_mes.append({ # type: ignore
                    "Codigo":str(cod_rep), # type: ignore
                    "Repuesto":rep,
                    "FechaCompleta":fecha,
                    "TotalMes":total_repuesto_mes
                })

            minimo = round(total_repuesto_final/len(fecha_rango_unico), 1)
            lista_totales_rep.append({#type: ignore
                " ":"",
                "CodigoUnico":str(cod_rep), # type: ignore
                "RepuestoUnico":rep,
                "Minimo": minimo*self.mult_por,
                "Maximo": minimo*(self.mult_por*2)
            })

        df_final = pd.concat((pd.DataFrame(lista_totales_mes), pd.DataFrame(lista_totales_rep)), axis=1) # type: ignore
        df_final.to_excel(f"{self._main_path}/excel/maxmin {self.fecha_hoy}.xlsx")


    def transformar_fecha_completa_a_fecha_mes(self, df):
        df["FechaCompleta"] = pd.DatetimeIndex(pd.to_datetime(df["FechaCompleta"])).strftime("%Y-%m")
        return df
        


if __name__ == "__main__":
    maxmin = MaxMin("maxmin", 2.5)
    maxmin.calcular_max_min()