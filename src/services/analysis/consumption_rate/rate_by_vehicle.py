import pandas as pd
import numpy as np

from typing import List, Union

from config import MAIN_PATH
from src.services.analysis.consumption_rate.utils.rate_utils import RateUtils
from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner


class RateByVehicle:
    def __init__(self, file: str, dir: str) -> None:
        self.file = file
        self.dir = dir

        self.df_vehicles = pd.read_excel(f"{MAIN_PATH}/src/data/excel_data/coches_por_cabecera.xlsx", engine="calamine")
        self.df_consumption = pd.read_excel(f"{MAIN_PATH}/out/{self.file}-S.xlsx", engine="calamine")


    def calculate_rate(self) -> List[Union[pd.DataFrame, str]]:
        InventoryDataCleaner(self.file, self.dir).run_all()

        grouped = self.df_consumption.groupby(['Cabecera', 'Repuesto']).agg({ # agrupo por columna
            'Cantidad':'sum', # le digo que quiero hacer en cada columna agrupada
            'Precio':'sum'
        }).reset_index()

        df_with_vehicles = grouped.merge(self.df_vehicles, on="Cabecera", how="left") # hago join con la cantidad de coches para hacer el cálculo
        df_with_vehicles["IndiceConsumo"] = round((df_with_vehicles["Cantidad"]*100) / df_with_vehicles["CantidadCoches"], 1) # hago el cálculo y se lo asigno a una nueva columna

        df_rate = df_with_vehicles.rename(columns={'Cantidad':'TotalConsumo',
                                                  'Precio':'TotalCoste'})[['Cabecera', 'Repuesto', 'TotalConsumo', 'TotalCoste', 'IndiceConsumo']]

        df_rate["IndiceConsumo"].replace([np.inf, -np.inf], np.nan, inplace=True)
        df_rate.dropna(subset=["IndiceConsumo"], inplace=True)

        df_rate.to_excel(f"{MAIN_PATH}/out/{self.file}_indice_por_coche.xlsx")
        return [df_rate, RateUtils()._create_title_date(self.df_consumption)]
