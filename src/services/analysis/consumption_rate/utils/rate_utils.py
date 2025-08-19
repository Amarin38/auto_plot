import pandas as pd

from numpy import ndarray
from typing import List


class RateUtils:
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
    def _create_title_date(df: pd.DataFrame) -> str:
        """
        Devuelve la fecha del titulo basandose en el file introducido.
        """
        df["FechaCompleta"] = pd.to_datetime(df["FechaCompleta"], errors="coerce")
        dates: ndarray = df["FechaCompleta"].unique()
        min_date = dates.min().strftime("%Y-%m")
        max_date = dates.max().strftime("%Y-%m")

        return f"{min_date} a {max_date}"
    
    @staticmethod
    def _create_months_list(diff_months) -> pd.Index:
        diff = pd.date_range(pd.Timestamp.today() - pd.Timedelta(days=30*diff_months))

        return pd.DatetimeIndex(diff.strftime("%Y-%B").unique())
