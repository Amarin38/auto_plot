import pandas as pd

from numpy import ndarray
from typing import List, Union
from enum import Enum

from config import OUT_PATH
from services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner
from services.utils.inventory_update import InventoryUpdate

class IndexTypeEnum(Enum):
    BY_MOTOR = "motor"
    BY_VEHICLE = "vehicle"


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
    def _create_title_date(df: pd.DataFrame) -> str:
        """
        Devuelve la fecha del titulo basandose en el file introducido.
        """
        df["FechaCompleta"] = pd.to_datetime(df["FechaCompleta"], errors="coerce", dayfirst=True)
        dates: ndarray = df["FechaCompleta"].unique()
        min_date = dates.min().strftime("%Y-%m")
        max_date = dates.max().strftime("%Y-%m")

        return f"{min_date} a {max_date}"
    
    
    @staticmethod
    def _create_months_list(diff_months) -> pd.Index:
        diff = pd.date_range(pd.Timestamp.today() - pd.Timedelta(days=30*diff_months))

        return pd.DatetimeIndex(diff.strftime("%Y-%B").unique())
    

    @staticmethod
    def _prepare_data(index_type: str, file, dir) -> List[pd.DataFrame | str]:
        from services.analysis.consumption_index.index_by_motor import IndexByMotor
        from services.analysis.consumption_index.index_by_vehicle import IndexByVehicle 

        InventoryDataCleaner(file, dir).run_all()

        if index_type == IndexTypeEnum.BY_MOTOR.value:
            df_updated = InventoryUpdate()._update_rows_by_dict(file, "motores")
            df_updated.to_excel(f"{OUT_PATH}/{file}-S.xlsx")
            index_list: List[Union[pd.DataFrame, str]] = IndexByMotor(file, dir).calculate_index()
        
        elif index_type == IndexTypeEnum.BY_VEHICLE.value:
            index_list: List[Union[pd.DataFrame, str]] = IndexByVehicle(file, dir).calculate_index()
        
        else:
            raise ValueError(f"Tipo de indice no soportado: {index_type}")

        return index_list
