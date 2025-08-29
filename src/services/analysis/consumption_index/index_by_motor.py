import pandas as pd
import numpy as np

from typing import List, Union

from config.constants import OUT_PATH, EXCEL_PATH
from services.utils.index_utils import IndexUtils
from services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner


class IndexByMotor:
    def __init__(self, file: str, dir: str) -> None:
        self.file = file
        self.dir = dir

        self.df_motors = pd.read_excel(f"{EXCEL_PATH}/motores_por_cabecera.xlsx", engine="calamine")
        self.df_consumption = pd.read_excel(f"{OUT_PATH}/{self.file}-S.xlsx", engine="calamine")


    def calculate_index(self) -> List[Union[pd.DataFrame, str]]:
        InventoryDataCleaner(self.file, self.dir).run_all()

        grouped = self.df_consumption.groupby(['Cabecera', 'Repuesto']).agg({'Cantidad':'sum'}).reset_index()

        df_with_vehicles = grouped.merge(self.df_motors, on=["Cabecera", "Repuesto"], how="right") # hago join con la cantidad de coches para hacer el cálculo
        df_with_vehicles["IndiceConsumo"] = round((df_with_vehicles["Cantidad"]*100) / df_with_vehicles["CantidadMotores"], 1) # hago el cálculo y se lo asigno a una nueva columna

        df_rate = df_with_vehicles[['Cabecera', 'Repuesto', 'IndiceConsumo']]
        df_rate["IndiceConsumo"].replace([np.inf, -np.inf], np.nan, inplace=True)
        df_rate.dropna(subset=["IndiceConsumo"], inplace=True)
        
        df_rate.to_excel(f"{OUT_PATH}/{self.file}_indice_por_motor.xlsx")
        return [df_rate, IndexUtils()._create_title_date(self.df_consumption)]


