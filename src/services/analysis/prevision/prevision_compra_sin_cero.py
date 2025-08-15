import pandas as pd
from typing import Union, Dict, List

from src.config import MAIN_PATH
from src.services.analysis import IndicePrevisionCompra, TendeciaPrevisionCompra

class PrevisionCompraSinCero:
    def __init__(self, archivo_xlsx: str, meses_en_adelante: int = 6) -> None:
        self.df = pd.read_excel(f"{MAIN_PATH}/out/{archivo_xlsx}.xlsx", engine="calamine")
        
        self.meses_en_adelante = meses_en_adelante
        self.repuestos = self.df["Repuesto"].unique()
        self.años = self.df["FechaCompleta"].dt.year.unique() 
        self.años_meses = (pd.date_range(start=f"1/1/{self.años[0]}", end=f"31/12/{self.años[-1]}", freq="ME")).to_period("M")

        self.tendencia = TendeciaPrevisionCompra(self.meses_en_adelante, self.repuestos, con_cero=False)
        self.indice = IndicePrevisionCompra(self.repuestos, con_cero=False)


    def calcular_prevision_compra(self) -> None:
        resultado: List[Dict[str, Union[pd.Period, int]]] = []
        fecha_periodo: pd.Series[pd.Period] = self.df["FechaCompleta"].dt.to_period("M")

        for rep in self.repuestos:
            suma_total_mes: int = 0
            for año_mes in self.años_meses:
                rep_comparado: pd.Series[bool] = self.df["Repuesto"] == rep
                año_comparado: pd.Series[bool] = fecha_periodo.dt.year == año_mes.year
                fecha_completa_comparada: pd.Series[bool] = fecha_periodo == año_mes
                
                suma_total_año = self.df.loc[rep_comparado & año_comparado, ["Cantidad"]].sum().iloc[0]
                suma_total_mes = self.df.loc[rep_comparado & fecha_completa_comparada, ["Cantidad"]].sum().iloc[0]
                
                resultado.append({
                    "Repuesto":rep,
                    "FechaCompleta":año_mes,
                    "Año":año_mes.year,
                    "Mes":año_mes.month,
                    "TotalAño":int(suma_total_año),
                    "TotalMes":int(suma_total_mes),
                })

        df_final = pd.DataFrame(resultado)
        
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

                suma_total_año = df.loc[rep_comparado & año_comparado, 
                                        ["TotalMes"]].sum().iloc[0]

                cont_sin_cero = df.loc[rep_comparado & año_comparado & 
                                       (df["TotalMes"] != 0)].count().iloc[0]

                if cont_sin_cero != 0:
                    promedio_sin_cero = suma_total_año/cont_sin_cero
                else:
                    promedio_sin_cero = 0.0
        
                resultado.append(round(float(promedio_sin_cero), 1))
        return resultado


    