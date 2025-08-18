import pandas as pd
import numpy as np
from numpy.polynomial import Polynomial

from typing import List, Dict, Union, Any

from src.services import PrevisionUtils

class TendeciaPrevisionCompra:
    def __init__(self, meses_en_adelante: int, repuestos, con_cero: bool) -> None:
        self.meses_en_adelante = meses_en_adelante
        self.repuestos = repuestos
        self.con_cero = con_cero


    def calcular(self, df: pd.DataFrame) -> pd.DataFrame:
        meses_en_adelante = PrevisionUtils._calcular_fecha_tendencia(self.meses_en_adelante)
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
                    indice_estacional_mes: int = df.loc[rep_comparado_df & mes_comparado_df, 
                                                        "IndiceEstacionalConCero"].iloc[0]
                else:
                    indice_estacional_mes: int = df.loc[rep_comparado_df & mes_comparado_df, 
                                                        "IndiceEstacionalSinCero"].iloc[0]
                    
                tendencia_mes: pd.Series[int] = df_tendencia.loc[rep_comparado_tendencia & mes_comparado_tendencia, "Tendencia"]

                tendencia_estacional.append(round((indice_estacional_mes * tendencia_mes).iloc[0], 0))
        
        return tendencia_estacional
