import pandas as pd

from src.config.constants import OUT_PATH, TODAY_FOR_DELTA 
from src.config.enums import WithZeroEnum

from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner

class ForecastUtils:
    @staticmethod
    def _calculate_date_trend(meses_en_adelante: int) -> pd.PeriodIndex:
        dias_en_adelante: int = 30 * (meses_en_adelante + 1)
        fecha_inicio: pd.Timestamp = TODAY_FOR_DELTA + pd.Timedelta(days=1)
        fecha_final: pd.Timestamp = TODAY_FOR_DELTA + pd.Timedelta(days=dias_en_adelante)

        return pd.date_range(fecha_inicio, fecha_final, freq="ME").to_period("M")


    @staticmethod
    def _convert_complete_date(tipo: str, fecha_completa: str) -> int:
        fecha: pd.Timestamp = pd.to_datetime(fecha_completa, format="%Y-%m")
        
        if tipo == "año":
            return fecha.year
        elif tipo == "mes":
            return fecha.month
        else:
            return fecha.day


    @staticmethod
    def prepare_data(file: str, directory: str, with_zero: str, months_to_forecast: int = 6) -> tuple[pd.DataFrame, pd.DataFrame]:
        from src.services.analysis.forecast.forecast_without_zero import ForecastWithoutZero
        from src.services.analysis.forecast.forecast_with_zero import ForecastWithZero

        """
        ### Prepara los datos para graficar.
        """
        InventoryDataCleaner(file, directory).run_all()

        if with_zero == WithZeroEnum.ZERO:
            ForecastWithZero(file, directory, months_to_forecast).calculate_forecast()
            df_tendencia = pd.read_excel(f"{OUT_PATH}/tendencia_ConCero.xlsx")
            df_data = pd.read_excel(f"{OUT_PATH}/data_ConCero.xlsx")
        elif with_zero == WithZeroEnum.NON_ZERO:
            ForecastWithoutZero(file, directory, months_to_forecast).calculate_forecast()
            df_tendencia = pd.read_excel(f"{OUT_PATH}/tendencia_SinCero.xlsx")
            df_data = pd.read_excel(f"{OUT_PATH}/data_SinCero.xlsx")
        else:
            raise ValueError(f"Por favor introduzca si es con o sin cero.")

        return df_tendencia, df_data
