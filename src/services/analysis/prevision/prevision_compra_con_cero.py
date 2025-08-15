import pandas as pd
from typing import Union, Dict, List

from src.config import MAIN_PATH
from src.services.analysis import IndicePrevisionCompra, TendeciaPrevisionCompra

class PrevisionCompraConCero:
    def __init__(self, archivo_xlsx: str, meses_en_adelante: int = 6) -> None:
        self.df = pd.read_excel(f"{MAIN_PATH}/out/{archivo_xlsx}.xlsx", engine="calamine")
        
        self.meses_en_adelante = meses_en_adelante
        self.repuestos = self.df["Repuesto"].unique()
        self.años = self.df["FechaCompleta"].dt.year.unique() 
        self.años_meses = (pd.date_range(start=f"1/1/{self.años[0]}", end=f"31/12/{self.años[-1]}", freq="ME")).to_period("M")

        self.tendencia = TendeciaPrevisionCompra(self.meses_en_adelante, self.repuestos, con_cero=True)
        self.indice = IndicePrevisionCompra(self.repuestos, con_cero=True)


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
                    "TotalAño":int(suma_total_año),
                    "TotalMes":int(suma_total_mes),
                })
                res_promedio_con_cero.append(round(promedio_con_cero, 1))

        df_final = pd.DataFrame(resultado)

        df_final["PromedioConCero"] = res_promedio_con_cero
        df_final["IndiceAnualConCero"] = self.indice.calcular_anual(df_final)
        df_final["IndiceEstacionalConCero"] = self.indice.calcular_estacional(df_final)
        df_final.to_excel(f"{MAIN_PATH}/out/data-ConCero.xlsx")

        df_tendencia: pd.DataFrame = pd.DataFrame(self.tendencia.calcular(df_final))
        df_tendencia["TendenciaEstacionalConCero"] = self.tendencia.calcular_estacional(df_final, df_tendencia)
        df_tendencia.to_excel(f"{MAIN_PATH}/out/tendencia-ConCero.xlsx")
