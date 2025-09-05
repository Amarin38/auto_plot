import pandas as pd
import numpy as np

from typing import Optional, Union

from src.config.constants import OUT_PATH, EXCEL_PATH
from src.services.utils.exception_utils import execute_safely
from src.db.crud import df_to_sql
from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner
from src.services.utils.common_utils import CommonUtils

class IndexByVehicle:
    def __init__(self, file: Union[pd.DataFrame, str], directory: str, tipo: str, filtro: Optional[str] = None) -> None:
        self.file = file
        self.directory = directory
        self.tipo = tipo
        self.filtro = filtro
        self.df_vehicles = pd.read_excel(f"{EXCEL_PATH}/coches_por_cabecera.xlsx", engine="calamine")
        # self.df_consumption = pd.read_excel(f"{OUT_PATH}/{self.file}-S.xlsx", engine="calamine")
        self.df_consumption = CommonUtils().convert_to_df(self.file)

    @execute_safely
    def calculate_index(self) -> None:
        if self.df_consumption is not None:
            fecha_max = self.df_consumption["FechaCompleta"].max()
            self.df_consumption["Cantidad"] = pd.to_numeric(self.df_consumption["Cantidad"], errors="coerce") 
            self.df_consumption["Precio"] = self.df_consumption["Precio"].astype(str).str.replace(",",".")
            self.df_consumption["Precio"] = pd.to_numeric(self.df_consumption["Precio"], errors="coerce")
            
            self.df_consumption["Precio"] = self.df_consumption["Cantidad"] * self.df_consumption["Precio"] 
            
            grouped = self.df_consumption.groupby(['Cabecera', 'Repuesto']).agg({'Cantidad':'sum', 'Precio':'sum'}).reset_index()

            df_with_vehicles = grouped.merge(self.df_vehicles, on="Cabecera", how="left") # hago join con la cantidad de coches para hacer el cálculo
            df_with_vehicles['IndiceConsumo'] = (df_with_vehicles["Cantidad"]*100) / df_with_vehicles["CantidadCoches"] # hago el cálculo y se lo asigno a una nueva columna

            df_rate = df_with_vehicles.rename(columns={'Cantidad':'TotalConsumo',
                                                       'Precio':'TotalCoste'})[['Cabecera', 'Repuesto', 'TotalConsumo', 'TotalCoste', 'IndiceConsumo']]

            # Modificaciones
            df_rate['TotalCoste'] = df_rate['TotalCoste'].round(0)
            df_rate['IndiceConsumo'] = df_rate["IndiceConsumo"].replace([np.inf, -np.inf], np.nan).round(1)
            df_rate['UltimaFecha'] = fecha_max
            df_rate['UltimaFecha'] = df_rate['UltimaFecha'].dt.date

            df_rate.dropna(subset=['IndiceConsumo'], inplace=True)
            df_rate.insert(2, 'TipoRepuesto', self.tipo)
            print(df_rate)

        if self.filtro is not None:
            df_rate = InventoryDataCleaner(df_rate).filter("Repuesto", self.filtro, "startswith")

        df_to_sql("indice_repuesto", df_rate) # guardo directoryecto en la base de datos
