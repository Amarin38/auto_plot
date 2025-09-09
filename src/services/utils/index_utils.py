import pandas as pd

from numpy import ndarray
from typing import List, Optional
from enum import Enum

from src.config.constants import OUT_PATH, TODAY_FOR_DELTA
from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner
from src.services.utils.inventory_update import InventoryUpdate




class IndexUtils:
    @staticmethod
    def _calculate_average(consumpt_rate: List[int], with_zero: bool) -> float:
        total_consumpt = sum(consumpt_rate)
        rates_quantity = 0

        if with_zero:
            rates_quantity = len(consumpt_rate)
        else:
            for indice in consumpt_rate:
                if indice != 0:
                    rates_quantity += 1
            

        if rates_quantity != 0:
            return round(total_consumpt/rates_quantity,2)
        else:
            return 0

    
    @staticmethod
    def create_title_date(df: pd.DataFrame) -> str:
        """
        Devuelve la fecha del titulo basandose en el file introducido.
        """
        dates: ndarray = df["Fecha"].unique()
        return f"{dates.min()} a {dates.max()}"
    
    
    @staticmethod
    def create_months_list(diff_months) -> pd.Index:
        diff = pd.date_range(TODAY_FOR_DELTA - pd.Timedelta(days=30*diff_months))

        return pd.DatetimeIndex(diff.strftime("%Y-%B").unique())
    

    

