import pandas as pd
import numpy as np
from numpy.polynomial import Polynomial

from typing import List, Dict, Union, Any

from src.services.utils.forecast_utils import ForecastUtils

class ForecastTrend:
    def __init__(self, meses_en_adelante: int, repuestos, con_cero: bool) -> None:
        self.meses_en_adelante = meses_en_adelante
        self.repuestos = repuestos
        self.con_cero = con_cero


    def calculate_trend(self, df: pd.DataFrame) -> pd.DataFrame:
        utils = ForecastUtils()
        meses_en_adelante = utils._calculate_date_trend(self.meses_en_adelante)
        resultado: List[Dict[str, Union[Any, int]]] = []

        for rep in self.repuestos:
            rep_comparado = df["Repuesto"] == rep
            
            x_cantidad_indices: np.ndarray = np.arange(df.loc[rep_comparado ,["TotalMes"]].count().iloc[0])
            y_consumo_conocido: Any = df.loc[rep_comparado, "TotalMes"]

            indice_inicio = len(x_cantidad_indices)
            indice_mes = np.arange(indice_inicio, indice_inicio + self.meses_en_adelante)

            poly = Polynomial.fit(x_cantidad_indices, y_consumo_conocido, deg=1).convert() # calculo tendencia lineal
            
            interseccion = poly.coef[0]
            pendiente = poly.coef[1]

            meses_prediccion = np.maximum(pendiente * indice_mes + interseccion, 0) # calculo los siguientes meses

            meses_iter = iter(meses_en_adelante.tolist()) # itero sobre las fechas por cada vuelta
            for prediccion in meses_prediccion:
                fecha_completa = next(meses_iter, None)
                resultado.append({
                    "Repuesto":rep,
                    "FechaCompleta":str(fecha_completa),
                    "Año":utils._convert_complete_date("año", fecha_completa), # type: ignore
                    "Mes":utils._convert_complete_date("mes", fecha_completa), # type: ignore
                    "Tendencia":prediccion
                    })
        
        return pd.DataFrame(resultado)


    # FIXME: hacer funcional como principal
    def calcular_v2(self, df:pd.DataFrame) -> pd.DataFrame:
        utils = ForecastUtils()
        meses_en_adelante = utils._calculate_date_trend(self.meses_en_adelante)
        resultado: List[Dict[str, Union[Any, int]]] = []

        df["Contado"] = ""

        x_cantidad_indices = df.groupby(["Repuesto", "TotalMes"]).agg({"Contado":"count"})
        y_consumo_conocido = x_cantidad_indices["Repuesto", "TotalMes"]

        indice_inicio = x_cantidad_indices.count()
        indice_mes = np.arange(indice_inicio, indice_inicio + self.meses_en_adelante)

        poly = Polynomial.fit(x_cantidad_indices, y_consumo_conocido, deg=1).convert() # calculo tendencia lineal
        
        interseccion = poly.coef[0]
        pendiente = poly.coef[1]

        meses_prediccion = np.maximum(pendiente * indice_mes + interseccion, 0) # calculo los siguientes meses

        meses_iter = iter(meses_en_adelante.tolist()) # itero sobre las fechas por cada vuelta
        
        
        return pd.DataFrame(resultado)
        

    def calculate_seasonal_rate(self, df_indice: pd.DataFrame, df_tendencia: pd.DataFrame) -> List[float]:
        indice_mes: List[str] = df_tendencia["Mes"].unique().tolist()
    
        tendencia_estacional: List[float] = []

        for rep in self.repuestos:
            rep_comparado_tendencia: pd.Series[bool] = df_tendencia["Repuesto"] == rep
            rep_comparado_df: pd.Series[bool] = df_indice["Repuesto"] == rep

            for mes in indice_mes:
                mes_comparado_tendencia: pd.Series[bool] = df_tendencia["Mes"] == mes
                mes_comparado_df: pd.Series[bool] = df_indice["Mes"] == mes
                
                indice_estacional_mes: int = df_indice.loc[rep_comparado_df & mes_comparado_df, 
                                                           "IndiceEstacional"].iloc[0]
                
                # if self.con_cero:
                #     indice_estacional_mes: int = df_indice.loc[rep_comparado_df & mes_comparado_df, 
                #                                         "IndiceEstacionalConCero"].iloc[0]
                # else:
                #     indice_estacional_mes: int = df_indice.loc[rep_comparado_df & mes_comparado_df, 
                #                                         "IndiceEstacionalSinCero"].iloc[0]
                    
                tendencia_mes: pd.Series[int] = df_tendencia.loc[rep_comparado_tendencia & 
                                                                 mes_comparado_tendencia, "Tendencia"]

                tendencia_estacional.append(round((indice_estacional_mes * tendencia_mes).iloc[0], 0))
        
        return tendencia_estacional
    

    # FIXME: hacer funcional como principal 
    def calculate_seasonal_rate_v2(self, df_indice: pd.DataFrame, df_tendencia: pd.DataFrame) -> List[float]:
        df_indice_agrupado = df_indice.groupby(["Repuesto", "Mes"]).agg({"IndiceEstacional":"sum"})
        df_tendencia_agrupada = df_tendencia.groupby(["Repuesto", "Mes"]).agg({"Tendencia":"sum"}) 
        
        df_final = pd.DataFrame()
        df_final["Multiplicado"] = round((df_indice_agrupado *  df_tendencia_agrupada), 0)

        return df_final["Multiplicado"].to_list()