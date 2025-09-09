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


