import pandas as pd

from typing import List

class ForecastRate:
    def __init__(self, repuestos, con_cero: bool) -> None:
        self.repuestos = repuestos
        self.con_cero = con_cero


    def calculate_anual_rate(self, df: pd.DataFrame) -> pd.Series:
        if self.con_cero:
            return round((df["TotalMes"] / df["PromedioConCero"]).where(df["PromedioConCero"] != 0, 0), 2)
        else:
            return round((df["TotalMes"] / df["PromedioSinCero"]).where(df["PromedioSinCero"] != 0, 0), 2)


    def calculate_seasonal_rate(self, df: pd.DataFrame) -> List[float]:
        años = df["Año"].unique()
        meses = df["Mes"].unique()

        resultado: List[float] = []

        for rep in self.repuestos:
            for año in años:
                for mes in meses:
                    rep_comparado = df["Repuesto"] == rep
                    mes_comparado = df["Mes"] == mes

                    if self.con_cero:
                        resultado.append(float(df.loc[rep_comparado & mes_comparado, 
                                                      ["IndiceAnualConCero"]].sum().iloc[0] / len(años)))
                    else:
                        resultado.append(float(df.loc[rep_comparado & mes_comparado, 
                                                      ["IndiceAnualSinCero"]].sum().iloc[0] / len(años)))
        return resultado


    # TODO probar si funciona 
    def calcular_estacional_v2(self, df: pd.DataFrame) -> pd.DataFrame:
        años = df["Año"].unique()

        if self.con_cero:
            agrupado = df.groupby(["Repuesto", "Mes"]).agg({"IndiceAnualConCero":"sum"})
            agrupado["IndiceAnualConCero"] = agrupado["IndiceAnualConCero"] / len(años) 
        else:
            agrupado = df.groupby(["Repuesto", "Mes"]).agg({"IndiceAnualSinCero":"sum"})
            agrupado["IndiceAnualSinCero"] = agrupado["IndiceAnualSinCero"] / len(años)  
        
        return agrupado
