import pandas as pd
import numpy as np
from typing import Union, Dict, List, Any

from numpy import ndarray
from numpy.polynomial import Polynomial

from src.config import MAIN_PATH
from src.services import PrevisionUtils

class CalcularPrevisionCompra:
    def __init__(self, archivo_xlsx: str, con_cero: bool, meses_en_adelante: int = 6) -> None:
        self.df = pd.read_excel(f"{MAIN_PATH}/out/{archivo_xlsx}.xlsx", engine="calamine")
        
        self.con_cero = con_cero

        self.meses_en_adelante = meses_en_adelante
        self.repuestos = self.df["Repuesto"].unique()
        self.años = self.df["FechaCompleta"].dt.year.unique() 
        self.años_meses = (pd.date_range(start=f"1/1/{self.años[0]}", end=f"31/12/{self.años[-1]}", freq="ME")).to_period("M")

        self.tendencia = CalcularTendecia(self.meses_en_adelante, self.repuestos, self.con_cero)
        self.indice = CalcularIndice(self.repuestos, self.con_cero)


    def calcular_prevision_compra(self) -> None:
        fecha_periodo: pd.Series[pd.Period] = self.df["FechaCompleta"].dt.to_period("M")

        resultado: List[Dict[str, Union[pd.Period, int]]] = []
        res_promedio_con_cero: List[float] = []

        for rep in self.repuestos:
            suma_total_mes: int = 0
            for año_mes in self.años_meses:
                rep_comparado: pd.Series[bool] = self.df["Repuesto"] == rep
                año_comparado: pd.Series[bool] = fecha_periodo.dt.year == año_mes.year
                fecha_completa_comparada: pd.Series[bool] = fecha_periodo == año_mes
                
                suma_total_año = self.df.loc[rep_comparado & año_comparado, ["Cantidad"]].sum().iloc[0]
                suma_total_mes = self.df.loc[rep_comparado & fecha_completa_comparada, ["Cantidad"]].sum().iloc[0]
                
                promedio_con_cero = suma_total_año/12

                resultado.append({
                    "Repuesto":rep,
                    "FechaCompleta":año_mes,
                    "Año":año_mes.year,
                    "Mes":año_mes.month,
                    # "TotalAño":int(suma_total_año),
                    "TotalMes":int(suma_total_mes),
                    # "PromedioConCero":round(promedio_con_cero, 1)
                })

                res_promedio_con_cero.append(round(promedio_con_cero, 1))

        df_final = pd.DataFrame(resultado)
        if self.con_cero:
            df_final["PromedioConCero"] = res_promedio_con_cero
            df_final["IndiceAnualConCero"] = self.indice.calcular_anual(df_final)
            df_final["IndiceEstacionalConCero"] = self.indice.calcular_estacional(df_final)
            df_final.to_excel(f"{MAIN_PATH}/out/data-ConCero.xlsx")

            df_tendencia: pd.DataFrame = pd.DataFrame(self.tendencia.calcular(df_final))
            df_tendencia["TendenciaEstacionalConCero"] = self.tendencia.calcular_estacional(df_final, df_tendencia)
            df_tendencia.to_excel(f"{MAIN_PATH}/out/tendencia-ConCero.xlsx")

        else:
            df_final["PromedioSinCero"] = self.calcular_sin_cero(df_final)
            df_final["IndiceAnualSinCero"] = self.indice.calcular_anual(df_final)
            df_final["IndiceEstacionalSinCero"] = self.indice.calcular_estacional(df_final)
            df_final.to_excel(f"{MAIN_PATH}/out/data-SinCero.xlsx")
            
            df_tendencia: pd.DataFrame = pd.DataFrame(self.tendencia.calcular(df_final))
            df_tendencia["TendenciaEstacionalSinCero"] = self.tendencia.calcular_estacional(df_final, df_tendencia)
            df_tendencia.to_excel(f"{MAIN_PATH}/out/tendencia-SinCero.xlsx")


    def calcular_sin_cero(self, df: pd.DataFrame) -> List[float]:
        resultado: List[float] = []

        for rep in self.repuestos:
            for año_mes in self.años_meses:
                cont_sin_cero: int = 0

                rep_comparado: pd.Series[bool] = df["Repuesto"] == rep
                año_comparado: pd.Series[bool] = df["Año"] == año_mes.year

                suma_total_año = df.loc[rep_comparado & 
                                        año_comparado, 
                                        ["TotalMes"]].sum().iloc[0]

                cont_sin_cero = df.loc[rep_comparado & 
                                       año_comparado & 
                                       (df["TotalMes"] != 0)].count().iloc[0]

                if cont_sin_cero != 0:
                    promedio_sin_cero = suma_total_año/cont_sin_cero
                else:
                    promedio_sin_cero = 0.0
        
                resultado.append(round(float(promedio_sin_cero), 1))
        return resultado


class CalcularIndice:
    def __init__(self, repuestos: ndarray, con_cero: bool) -> None:
        self.repuestos = repuestos
        self.con_cero = con_cero


    def calcular_anual(self, df: pd.DataFrame) -> pd.Series:
        if self.con_cero:
            return round((df["TotalMes"] / df["PromedioConCero"]).where(df["PromedioConCero"] != 0, 0), 2)
        else:
            return round((df["TotalMes"] / df["PromedioSinCero"]).where(df["PromedioSinCero"] != 0, 0), 2)


    def calcular_estacional(self, df: pd.DataFrame) -> List[float]:
        años = df["Año"].unique()
        meses = df["Mes"].unique()

        resultado: List[float] = []

        for rep in self.repuestos:
            for año in años:
                for mes in meses:
                    rep_comparado = df["Repuesto"] == rep
                    mes_comparado = df["Mes"] == mes

                    if self.con_cero:
                        resultado.append(float(df.loc[rep_comparado & 
                                                      mes_comparado, 
                                                      ["IndiceAnualConCero"]].sum().iloc[0] / len(años)
                                                      ))
                    else:
                        resultado.append(float(df.loc[rep_comparado & 
                                                      mes_comparado, 
                                                      ["IndiceAnualSinCero"]].sum().iloc[0] / len(años)
                                                      ))
        return resultado


class CalcularTendecia:
    def __init__(self, meses_en_adelante: int, repuestos: ndarray, con_cero: bool) -> None:
        self.meses_en_adelante = meses_en_adelante
        self.repuestos = repuestos
        self.con_cero = con_cero


    def calcular(self, df: pd.DataFrame) -> pd.DataFrame:
        meses_en_adelante = PrevisionUtils._calcular_fecha_tendencia(self.meses_en_adelante)
        resultado: List[Dict[str, Union[Any, int]]] = []

        # -------------------------
        for rep in self.repuestos:
            rep_comparado = df["Repuesto"] == rep
            
            x_cantidad_indices: ndarray = np.arange(df.loc[rep_comparado ,["TotalMes"]].count().iloc[0])
            y_consumo_conocido: Any = df.loc[rep_comparado, "TotalMes"]

            indice_inicio = len(x_cantidad_indices)
            indice_mes = np.arange(indice_inicio, indice_inicio + self.meses_en_adelante)

            poly = Polynomial.fit(x_cantidad_indices, y_consumo_conocido, deg=1).convert() # calculo tendencia lineal
            
            interseccion = poly.coef[0]
            pendiente = poly.coef[1]

            meses_prediccion = np.maximum(pendiente * indice_mes + interseccion, 0) # calculo los siguientes meses

            meses_iter = iter(meses_en_adelante.tolist()) # itero sobre las fechas por cada vuelta
            for prediccion in meses_prediccion:
                fecha_completa = next(meses_iter)
                resultado.append({
                    "Repuesto":rep,
                    "FechaCompleta":fecha_completa,
                    "Año":self.fecha_completa_a("año", fecha_completa), # type: ignore
                    "Mes":self.fecha_completa_a("mes", fecha_completa), # type: ignore
                    "Tendencia":prediccion
                    })
        
        return pd.DataFrame(resultado)


    def calcular_estacional(self, df: pd.DataFrame, df_tendencia: pd.DataFrame) -> List[float]:
        indice_mes: List[str] = df_tendencia["Mes"].unique().tolist()
    
        tendencia_estacional: List[float] = []

        for rep in self.repuestos:
            rep_comparado_tendencia: pd.Series[bool] = df_tendencia["Repuesto"] == rep
            rep_comparado_df: pd.Series[bool] = df["Repuesto"] == rep

            for mes in indice_mes:
                mes_comparado_tendencia: pd.Series[bool] = df_tendencia["Mes"] == mes
                mes_comparado_df: pd.Series[bool] = df["Mes"] == mes
                
                if self.con_cero:
                    indice_estacional_mes: int = df.loc[rep_comparado_df & 
                                                        mes_comparado_df, 
                                                        "IndiceEstacionalConCero"].iloc[0]
                else:
                    indice_estacional_mes: int = df.loc[rep_comparado_df & 
                                                        mes_comparado_df, 
                                                        "IndiceEstacionalSinCero"].iloc[0]
                    
                tendencia_mes: pd.Series[int] = df_tendencia.loc[rep_comparado_tendencia & 
                                                                 mes_comparado_tendencia, 
                                                                 "Tendencia"]

                tendencia_estacional.append(round((indice_estacional_mes * tendencia_mes).iloc[0], 0))
        
        return tendencia_estacional
    