import pandas as pd

from typing import List

class ForecastIndex:
    def __init__(self, repuestos, con_cero: bool) -> None:
        self.repuestos = repuestos
        self.con_cero = con_cero


    def calculate_anual_rate(self, df: pd.DataFrame) -> pd.Series:
        if self.con_cero:
            return round((df["TotalMes"] / df["PromedioConCero"]).where(df["PromedioConCero"] != 0, 0), 2)
        else:
            return round((df["TotalMes"] / df["PromedioSinCero"]).where(df["PromedioSinCero"] != 0, 0), 2)


    def calculate_anual_rate_v2(self, df: pd.DataFrame) -> pd.Series:
        return round((df["TotalMes"] / df["Promedio"]).where(df["Promedio"] != 0, 0), 2)


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


    def calculate_seasonal_rate_v2(self, df: pd.DataFrame) -> List[float]:
        años = df["Año"].unique()

        agrupado = df.groupby(["Repuesto", "Mes"]).agg({"IndiceAnual":"sum"}).reset_index()
        agrupado["IndiceAnual"] = agrupado["IndiceAnual"] / len(años)

        return agrupado["IndiceAnual"].to_list()