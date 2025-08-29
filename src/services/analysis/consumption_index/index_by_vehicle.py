import pandas as pd
import numpy as np

from typing import List, Union

from config import OUT_PATH, EXCEL_PATH
from services.utils.index_utils import IndexUtils
from services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner
from services.utils.exception_utils import execute_safely

class IndexByVehicle:
    def __init__(self, file: str, dir: str) -> None:
        self.file = file
        self.dir = dir

        self.df_vehicles = pd.read_excel(f"{EXCEL_PATH}/coches_por_cabecera.xlsx", engine="calamine")
        self.df_consumption = pd.read_excel(f"{OUT_PATH}/{self.file}-S.xlsx", engine="calamine")

    @execute_safely
    def calculate_index(self) -> List[Union[pd.DataFrame, str]]:
        self.df_consumption["Cantidad"] = pd.to_numeric(self.df_consumption["Cantidad"], errors="coerce")
        self.df_consumption["Precio"] = self.df_consumption["Precio"].astype(str).str.replace(",",".")
        self.df_consumption["Precio"] = pd.to_numeric(self.df_consumption["Precio"], errors="coerce")

        self.df_consumption["Precio"] = self.df_consumption["Cantidad"] * self.df_consumption["Precio"] 
        
        grouped = self.df_consumption.groupby(['Cabecera', 'Repuesto']).agg({'Cantidad':'sum', 'Precio':'sum'}).reset_index()

        df_with_vehicles = grouped.merge(self.df_vehicles, on="Cabecera", how="left") # hago join con la cantidad de coches para hacer el cálculo
        df_with_vehicles["IndiceConsumo"] = round((df_with_vehicles["Cantidad"]*100) / df_with_vehicles["CantidadCoches"], 1) # hago el cálculo y se lo asigno a una nueva columna

        df_rate = df_with_vehicles.rename(columns={'Cantidad':'TotalConsumo',
                                                   'Precio':'TotalCoste'})[['Cabecera', 'Repuesto', 'TotalConsumo', 'TotalCoste', 'IndiceConsumo']]

        
        df_rate['IndiceConsumo'] = df_rate["IndiceConsumo"].replace([np.inf, -np.inf], np.nan) 
        df_rate.dropna(subset=["IndiceConsumo"], inplace=True)

        df_rate.to_excel(f"{OUT_PATH}/{self.file}_indice_por_coche.xlsx")
        return [df_rate, IndexUtils()._create_title_date(self.df_consumption)]
