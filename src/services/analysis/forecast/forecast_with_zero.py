import pandas as pd
from typing import Union, Dict, List

from config.constants import OUT_PATH
from services.utils.forecast_index import ForecastIndex 
from services.utils.forecast_trend import ForecastTrend
from services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner


# TODO: cambiar a groupby 
class ForecastWithZero:
    def __init__(self, file: str, dir: str, meses_en_adelante: int = 6) -> None:
        self.df = pd.read_excel(f"{OUT_PATH}/{file}.xlsx", engine="calamine")
        
        self.meses_en_adelante = meses_en_adelante
        self.repuestos = self.df["Repuesto"].unique()
        self.años = self.df["FechaCompleta"].dt.year.unique() 
        self.años_meses = (pd.date_range(start=f"1/1/{self.años[0]}", end=f"31/12/{self.años[-1]}", freq="ME")).to_period("M")

        self.tendencia = ForecastTrend(self.meses_en_adelante, self.repuestos, con_cero=True)
        self.indice = ForecastIndex(self.repuestos, con_cero=True)
        self.listado = InventoryDataCleaner(file, dir)

    def calculate_forecast(self) -> None:
        self.listado.run_all()
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
        df_final["IndiceAnualConCero"] = self.indice.calculate_anual_rate(df_final)
        df_final["IndiceEstacionalConCero"] = self.indice.calculate_seasonal_rate(df_final)
        df_final.to_excel(f"{OUT_PATH}/data-ConCero.xlsx")

        df_tendencia: pd.DataFrame = pd.DataFrame(self.tendencia.calculate_trend(df_final))
        df_tendencia["TendenciaEstacionalConCero"] = self.tendencia.calculate_seasonal_rate(df_final, df_tendencia)
        df_final.to_excel(f"{OUT_PATH}/tendencia-ConCero.xlsx")
