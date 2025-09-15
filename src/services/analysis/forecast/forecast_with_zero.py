import pandas as pd
from typing import List

from src.services.analysis.forecast.forecast_index import ForecastIndex 
from src.services.analysis.forecast.forecast_trend import ForecastTrendModel
from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner
from src.db.crud_services import CRUDServices
from src.utils.exception_utils import execute_safely


# TODO: cambiar a groupby 
class ForecastWithZero:
    def __init__(self, df: pd.DataFrame, directory: str, type: str, months_to_forecast: int = 12) -> None:
        self.df = df
        self.directory = directory
        self.type = type
        self.months_to_forecast = months_to_forecast
        self.crud = CRUDServices()
    
        self.repuestos = df["Repuesto"].unique()
        self.años = df["FechaCompleta"].dt.year.unique()

        self.años_meses = pd.date_range(start=f"1/1/{self.años.min()}", end=f"31/12/{self.años.max()}", freq="ME").to_period("M")
        self.trend = ForecastTrendModel(self.months_to_forecast, self.repuestos, con_cero=True) # TODO: cambiar
        self.index = ForecastIndex(self.repuestos, con_cero=True) # TODO: cambiar
        self.inv_cleaner = InventoryDataCleaner()


    @execute_safely
    def create_forecast(self) -> None:
        self.inv_cleaner.run_all(self.directory)
        data = self._calculate_forecast()

        df_data = pd.DataFrame(data[0])
        df_data["Promedio"] = data[1]
        df_data["IndiceAnual"] = self.index.calculate_anual_rate(df_data)
        df_data["IndiceEstacional"] = self.index.calculate_seasonal_rate(df_data)
        df_data.insert(2, 'TipoRepuesto', self.type)

        df_trend = pd.DataFrame(self.trend.calculate_trend(df_data))
        df_trend["TendenciaEstacional"] = self.trend.calculate_seasonal_rate(df_data, df_trend)
        df_trend.insert(2, 'TipoRepuesto', self.type)

        # guardo el proyecto en la base de datos
        self.crud.df_to_db("forecast_data", df_data, "append") 
        self.crud.df_to_db("forecast_trend", df_trend, "append")


    @execute_safely
    def _calculate_forecast(self):
        result: List = []
        mean_reasult: List[float] = []

        period_date: pd.Series[pd.Period] = self.df["FechaCompleta"].dt.to_period("M")
    
        for rep in self.repuestos:
            month_sum: int = 0
            for año_mes in self.años_meses:
                rep_comparado: pd.Series[bool] = self.df["Repuesto"] == rep
                año_comparado: pd.Series[bool] = period_date.dt.year == año_mes.year
                fecha_completa_comparada: pd.Series[bool] = period_date == año_mes
                
                year_sum = self.df.loc[rep_comparado & año_comparado, ["Cantidad"]].sum().iloc[0]
                month_sum = self.df.loc[rep_comparado & fecha_completa_comparada, ["Cantidad"]].sum().iloc[0]
                
                promedio_con_cero = year_sum/12

                result.append({
                    "Repuesto":rep,
                    "FechaCompleta":str(año_mes),
                    "Año":año_mes.year,
                    "Mes":año_mes.month,
                    "TotalAño":int(year_sum),
                    "TotalMes":int(month_sum),
                })
                mean_reasult.append(round(promedio_con_cero, 1))
        
        return result, mean_reasult