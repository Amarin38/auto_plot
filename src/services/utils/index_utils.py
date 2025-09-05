import pandas as pd

from numpy import ndarray
from typing import List, Optional
from enum import Enum

from src.config.constants import OUT_PATH, TODAY_FOR_DELTA
from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner
from src.services.utils.inventory_update import InventoryUpdate

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
    

    @staticmethod
    def prepare_data(index_type: str, file: str, directory: str, tipo_repuesto: str, filtro: Optional[str] = None) -> None:
        from src.services.analysis.consumption_index.index_by_motor import IndexByMotor
        from src.services.analysis.consumption_index.index_by_vehicle import IndexByVehicle 

        df = InventoryDataCleaner(file, directory, save="NO GUARDAR").run_all()

        if index_type == IndexTypeEnum.BY_MOTOR.value:
            df_updated = InventoryUpdate(df)._update_rows_by_dict(file, "motores") #FIXME: le paso un file normal pero del otro lado es un json
            df_updated.to_excel(f"{OUT_PATH}/{file}-S.xlsx")
            
            IndexByMotor(file, directory, tipo_repuesto).calculate_index()
        
        
        elif index_type == IndexTypeEnum.BY_VEHICLE.value:
            IndexByVehicle(df, directory, tipo_repuesto, filtro).calculate_index()
        
        else:
            raise ValueError(f"Tipo de indice no soportado: {index_type}")

