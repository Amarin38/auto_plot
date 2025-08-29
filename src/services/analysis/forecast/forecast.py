import pandas as pd

from config.constants import OUT_PATH
from config.enums import WithZeroEnum
from src.services.analysis.forecast.forecast_index import ForecastIndex 
from src.services.analysis.forecast.forecast_trend import ForecastTrend
from services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner


class Forecast:
    def __init__(self, file: str, dir: str, 
                 with_zero: str = "con cero", meses_en_adelante: int = 6) -> None:
        self.file = file
        self.dir = dir
        self.with_zero = with_zero
        self.meses_en_adelante = meses_en_adelante
        self.df = pd.read_excel(f"{OUT_PATH}/{file}.xlsx", engine="calamine")

        self.repuestos = self.df["Repuesto"].unique()
        self.tendencia = ForecastTrend(self.meses_en_adelante, self.repuestos, con_cero=True)
        self.indice = ForecastIndex(self.repuestos, con_cero=True)


    def calculate_forecast(self) -> None:
        InventoryDataCleaner(self.file, self.dir).run_all()
        fecha_periodo: pd.Series[pd.Period] = self.df["FechaCompleta"].dt.to_period("M")

        self.df["fechaMes"] = fecha_periodo.dt.month
        self.df["fechaAño"] = fecha_periodo.dt.year
        self.df["TotalAño"] = self.df.groupby(["Repuesto", "fechaAño"]).agg({"Cantidad":"sum"}).reset_index()
        self.df["TotalMes"] = self.df.groupby(["Repuesto", "fechaMes"]).agg({"Cantidad":"sum"}).reset_index()
        self.df["Promedio"] = round(self.df["TotalAño"]/12, 1)
        self.df["IndiceAnual"] = self.indice.calculate_anual_rate(self.df)
        self.df["IndiceEstacional"] = self.indice.calculate_seasonal_rate(self.df)

        df_tendencia = pd.DataFrame(self.tendencia.calculate_trend(self.df))
        self.df["TendenciaEstacional"] = self.tendencia.calculate_seasonal_rate(self.df, df_tendencia)

        if self.with_zero == WithZeroEnum.ZERO:
            self.df.to_excel(f"{OUT_PATH}/tendencia_ConCero.xlsx")
        elif self.with_zero == WithZeroEnum.NON_ZERO:
            self.df.to_excel(f"{OUT_PATH}/tendencia_SinCero.xlsx")
        else:
            raise ValueError("Introduce un valor que sea con o sin cero.")