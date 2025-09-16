import pandas as pd

from src.config.enums import WithZeroEnum
from src.services.analysis.forecast.forecast_index import ForecastIndex 
from src.services.analysis.forecast.forecast_trend import ForecastTrendModel


class Forecast:
    def __init__(self, df: pd.DataFrame, with_zero: WithZeroEnum = WithZeroEnum.ZERO, meses_en_adelante: int = 6) -> None:
        self.df = df
        self.with_zero = with_zero
        self.meses_en_adelante = meses_en_adelante

        self.repuestos = self.df["Repuesto"].unique()
        self.tendencia = ForecastTrendModel(self.meses_en_adelante, self.repuestos, con_cero=True)
        self.indice = ForecastIndex(self.repuestos, con_cero=True)


    def calculate_forecast(self) -> pd.DataFrame:
        fecha_periodo: pd.Series[pd.Period] = self.df["FechaCompleta"].dt.to_period("M")

        self.df["fechaMes"] = fecha_periodo.dt.month
        self.df["fechaAño"] = fecha_periodo.dt.year
        self.df["TotalAño"] = self.df.groupby(["Repuesto", "fechaAño"]).agg({"Cantidad":"sum"}).reset_index()
        self.df["TotalMes"] = self.df.groupby(["Repuesto", "fechaMes"]).agg({"Cantidad":"sum"}).reset_index()
        self.df["Promedio"] = round(self.df["TotalAño"] / 12, 1)
        self.df["IndiceAnual"] = self.indice.calculate_anual_rate(self.df)
        self.df["IndiceEstacional"] = self.indice.calculate_seasonal_rate(self.df)

        df_tendencia = pd.DataFrame(self.tendencia.calculate_trend(self.df))
        self.df["TendenciaEstacional"] = self.tendencia.calculate_seasonal_rate(self.df, df_tendencia)

        return self.df