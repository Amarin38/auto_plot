import pandas as pd
import numpy as np

from typing import Optional

from src.utils.exception_utils import execute_safely
from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner

from src.db.crud_common import CRUDCommon

class IndexByVehicle:
    def __init__(self, ) -> None:
        self.crud = CRUDCommon()
        self.cleaner = InventoryDataCleaner()
        self.df_vehicles = self.crud.db_to_df("coches_cabecera")


    @execute_safely
    def calculate_index(self, df: pd.DataFrame, tipo: str, filtro: Optional[str] = None) -> None:
        if not df.empty:
            fecha_max = df["FechaCompleta"].max()

            df["Cantidad"] = pd.to_numeric(df["Cantidad"], errors="coerce") 
            df["Precio"] = df["Precio"].astype(str).str.replace(",",".")
            df["Precio"] = pd.to_numeric(df["Precio"], errors="coerce")
            
            df["Precio"] = df["Cantidad"] * df["Precio"] 
            
            grouped = df.groupby(['Cabecera', 'Repuesto']).agg({'Cantidad':'sum', 'Precio':'sum'}).reset_index()

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
            df_rate.insert(2, 'TipoRepuesto', tipo)

            if filtro is not None:
                df_rate = self.cleaner.filter(df_rate, "Repuesto", filtro, "startswith")

            self.crud.df_to_db("index_repuesto", df_rate, "append") # guardo el proyecto en la base de datos
        else:
            print("El df está vacío.")
